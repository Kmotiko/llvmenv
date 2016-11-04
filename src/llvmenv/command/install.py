#!/usr/bin/env python
import json
import os
from llvmenv.lib import common

class InstallSubcommand():
    llvm_opts = {
            "autotools":{
                "enable_targets": "--enable-targets",
                "enable_optimized": {
                    True: "--enable-optimized", 
                    False: "--disable-optimized"},
                "enable_assertions": {
                    True: "--enable-assertions", 
                    False: "--disable-assertions"}
                },
            "cmake":{
                "enable_targets": "-DLLVM_TARGETS_TO_BUILD",
                "enable_optimized": {
                    "key": "-DCMAKE_BUILD_TYPE", 
                    True: "RELEASE", 
                    False: "DEBUG"
                    },
                "enable_assertions": {
                    "key": "-DLLVM_ENABLE_ASSERTIONS", 
                    True: "ON", 
                    False: "OFF"},
                "build_examples": {
                    "key": "-DLLVM_BUILD_EXAMPLES", 
                    True: "ON", 
                    False: "OFF"},
                "build_tests": {
                    "key": "-DLLVM_BUILD_TESTS", 
                    True: "ON", 
                    False: "OFF"}
                }
            }
    clang_opts = {
            "cmake":{
                "build_examples": {
                    "key": "-DCLANG_BUILD_EXAMPLES", 
                    True: "ON", 
                    False: "OFF"}
                }
            }

    def __init__(self, opts):
        self._logger=common.get_logger()
        self._llvmenv_home = os.getenv('LLVMENV_HOME')
        self._options = opts

    def run(self):
        """
        run command
        """

        ########################################
        # pre check

        ########################################
        # check version
        #
        version_urls = self._is_available_version(self._options.version)
        if version_urls == None:
            return False
        ########################################
        # check exists directory
        #
        install_dir = os.path.join(self._llvmenv_home , 'llvms' , self._options.version)
        if os.path.exists(install_dir):
            self._logger.error('directory %s already exists' % install_dir)
            self._logger.error('nothing to do')
            return False

        ret = True
        try:
            build_base =  os.path.join(self._llvmenv_home , 'llvm_build' , self._options.version)
            if not os.path.exists( build_base ):
                os.makedirs(build_base) 

            build_dir =  os.path.join(build_base, 'build')
            if os.path.exists(build_dir):
                self._logger.warn('directory %s already exists' % build_dir)
                self._logger.warn('try to install from %s' % build_dir)

                self._configure(self._options.generator, self._options.builder)
                self._make(self._options.builder)
                os.makedirs(install_dir) 
                self._install(self._options.builder)
                return False

            ########################################
            # checkout
            #
            src_dir =  os.path.join(self._llvmenv_home , 'llvm_build' , self._options.version , 'llvm')
            if not os.path.exists(src_dir):
                self._checkout_all(self._options.version, version_urls)
            
            ########################################
            # configure
            #
            os.makedirs(build_dir) 
            self._configure(self._options.generator, self._options.builder, self._options.version)
            
            ########################################
            # make
            #
            self._make(self._options.builder, self._options.version)
            
            ########################################
            # make install
            #
            os.makedirs(install_dir) 
            self._install(self._options.builder, self._options.version)

            ret = True
        except Exception,e:
            self._logger.error(type(e))
            self._logger.error(e.__args__)
            ret = False
        finally:
            ########################################
            # clean up directory
            #
            self._clean_directory(self._options.version)
            return ret


    def _is_available_version(self, version):
        """
        check whether specified version is available or not
        """
        self._logger.info('start check available version')
        file_path =  os.path.join(self._llvmenv_home, 'etc', 'versions.json')
        ########################################
        # check file exists or not 
        #
        if os.path.exists(file_path) == False:
            self._logger.error('file %s was not found' % file_path)
            return None
        
        ########################################
        # check version
        #
        with open(file_path) as f:
            versions = json.loads(f.read(), encoding = 'utf-8')
            if versions.has_key(version):
                return versions[version]
            else:
                return None


    def _checkout(self, repo, version, target_dir):
        """
        """
        self._logger.info('start check out')
        cmd = ['svn', 'co']
        args = []
        args.append(repo)
        args.append(target_dir)
        self._logger.info('start cloning from %s ...' % repo)
        ret, out = common.exec_command(cmd + args)
        
        if not ret:
            self._logger.error(out)
            raise Exception('failed to check out from %s' % repo)

        return True

    def _checkout_all(self, version, urls):
        """
        checkout specified version
        """
        self._logger.info('start check out all')
        ########################################
        # 
        #
        if len(self._llvmenv_home) == 0:
            self._logger.error('env LLVMENV_HOME is not set')
            return False

        self._logger.info('set home directory ... %s' % self._llvmenv_home)

        ########################################
        # checkout llvm
        #
        llvm = os.path.join(self._llvmenv_home, 'llvm_build', version , 'llvm')
        self._checkout(urls['llvm'], version.replace('.','/'), llvm)

        ########################################
        # checkout clang
        #
        clang = os.path.join(llvm, 'tools', 'clang')
        self._checkout(urls['clang'], version.replace('.', '/'), clang)
        
        ########################################
        # checkout compiler-rt
        #
        compiler_rt = os.path.join(llvm, 'projects', 'compiler-rt')
        self._checkout(urls['compiler-rt'], version.replace('.', '/'), compiler_rt)


        if self._options.with_lldb == True and urls['lldb']:
            ########################################
            # checkout lldb
            #
            lldb = os.path.join(llvm, 'tools', 'lldb')
            self._checkout(urls['lldb'], version.replace('.', '/'), lldb)


        if self._options.with_libcxx == True and urls['libcxx']:
            ########################################
            # checkout libc++
            #
            libcxx = os.path.join(llvm, 'projects', 'libcxx')
            self._checkout(urls['libcxx'], version.replace('.', '/'), libcxx)

        if self._options.with_libcxxabi == True and urls['libcxxabi']:
            ########################################
            # checkout libc++abi
            #
            libcxxabi = os.path.join(llvm, 'projects', 'libcxxabi')
            self._checkout(urls['libcxxabi'], version.replace('.', '/'), libcxxabi)


        ########################################
        # clang-extra-tools
        #
        if urls['clang-extra']:
            extra = os.path.join(llvm, 'tools', 'clang', 'tools', 'extra')
            self._checkout(urls['clang-extra'], version.replace('.', '/'), extra)

        return


    def _configure(self, generator, builder, version):
        """
        exec configure
        """
        self._logger.info('start configure')
        build_dir =  self._llvmenv_home + '/llvm_build/' + version + '/build'

        ########################################
        # change directory
        #
        os.chdir(build_dir)

        ########################################
        # check generator
        #
        if generator != 'autotools' and generator != 'cmake':
            self._logger.warn('unknown generator : %s.' % generator)
            self._logger.info('use cmake')
            generator = 'cmake'

        ########################################
        # create cmd
        #
        if generator == 'autotools':
            cmd = [ os.path.join(self._llvmenv_home, 'llvm_build', version, 'llvm', 'configure' )]
        elif generator == 'cmake':
            cmd = [generator]
            if builder == 'ninja':
                cmd.append('-G')
                cmd.append('Ninja')
            cmd.append('../llvm')
        args = self._generate_opts(generator, version)
        self._logger.info('configure option is ... %s' % args)
        cmd += args
        if common.exec_command_with_call(cmd):
            raise Exception('failed to configure')
        return


    def _generate_opts(self, generator, version):
        opts = []
        if self._options.opt != '':
            opts = self._options.opt.split(' ')
        install_dir = os.path.join(self._llvmenv_home, 'llvms', version)
        if generator == 'cmake':
            for opt in opts:
                if opt.startswith('-DCMAKE_INSTALL_PREFIX') :
                    opts.remove(opt)

            opt_map = self.llvm_opts['cmake']
            copt_map = self.clang_opts['cmake']
            # enable_targets
            opt_str = '%s=%s' % (opt_map['enable_targets'], self._options.enable_targets)
            opts.append(opt_str)
            # build_type
            opt_str = '%s=%s' % (opt_map['enable_optimized']['key'], opt_map['enable_optimized'][self._options.enable_optimized])
            opts.append(opt_str)
            # enable_assertions
            opt_str = '%s=%s' % (opt_map['enable_assertions']['key'], opt_map['enable_assertions'][self._options.enable_assertions])
            opts.append(opt_str)
            # build_examples
            opt_str = '%s=%s' % (opt_map['build_examples']['key'], opt_map['build_examples'][self._options.build_examples])
            opts.append(opt_str)
            opt_str = '%s=%s' % (copt_map['build_examples']['key'], copt_map['build_examples'][self._options.build_examples])
            opts.append(opt_str)
            # build_tests
            opt_str = '%s=%s' % (opt_map['build_tests']['key'], opt_map['build_tests'][self._options.build_tests])
            opts.append(opt_str)
            opts.append('-DCMAKE_EXPORT_COMPILE_COMMANDS=ON') 
            opts.append('-DCMAKE_INSTALL_PREFIX=%s' % install_dir)

        elif generator=='autotools':
            for opt in opts:
                if opt.startswith('--prefix') :
                    opts.remove(opt)

            opt_map = llvm_opts['autotools']
            # enable_targets
            opt_str = '%s=%s' % (opt_map['enable_targets'], self._options.enable_targets)
            opts.append(opt_str)
            ## build_type
            opt_str = '%s' % (opt_map['enable_optimized'][self._options.enable_optimized])
            opts.append(opt_str)
            ## enable_assertions
            opt_str = '%s' % (opt_map['enable_assertions'][self._options.enable_optimized])
            opts.append(opt_str)
            opts.append('--prefix=%s' % install_dir)

        return opts

    def _make(self, builder, version):
        """
        exec make
        """
        self._logger.info('start build')

        ########################################
        # TODO: validate builder
        #


        ########################################
        # change directory
        #
        build_dir =  os.path.join(self._llvmenv_home, 'llvm_build', version, 'build')
        os.chdir(build_dir)

        ########################################
        # do make
        #
        cmd = [builder]
        if common.exec_command_with_call(cmd):
            raise Exception('failed to configure')
        return

    def _install(self, builder, version):
        """
        exec install
        """
        self._logger.info('start install')
        ########################################
        # change directory
        #
        build_dir =  self._llvmenv_home + '/llvm_build/' + version + '/build'
        os.chdir(build_dir)

        ########################################
        # do make install
        #
        cmd = [builder, 'install']
        if common.exec_command_with_call(cmd):
            raise Exception('failed to configure')
        return

    def _clean_directory(self, version):
        self._logger.info('start clean directory')
        ########################################
        # if delete-src is True, delete src dir
        #
        src_dir = os.path.join(self._llvmenv_home, 'llvm_build', version , 'llvm')
        if self._options.delete_src:
            common.remove_dir(src_dir)

        ########################################
        # if delete-obj is True, delete build
        #
        build_dir = os.path.join(self._llvmenv_home, 'llvm_build', version , 'build')
        if self._options.delete_build:
            common.remove_dir(build_dir)
        
        return
