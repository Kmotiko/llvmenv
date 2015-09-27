#!/usr/bin/env python
import os
import llvm_url
import shutil
from llvmenv.lib import common

class InstallSubcommand():
    _llvm_opts = {
            "autotools":{
                "enable_targets": "--enable_targets",
                "enable_optimized": {
                    True: "--enable-optimized", 
                    False: "--disable_optimized"},
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
    _clang_opts = {
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


    def _get_and_extract(self, url, download_dir = '/tmp/', extract_dir = '/tmp/'):
        # downlowd
        target_file = os.path.join(download_dir, os.path.basename(url))
        common.download(url, target_file)

        # decompress file
        if os.path.splitext(target_file)[1] == '.xz' : 
            common.decompress_xz(target_file)
        elif os.path.splitext(target_file)[1] == '.gz' : 
            print 'not support yet' # TODO: extract gz
        else :
            print 'unknown file type';# TODO: error processing

        # extract file
        decomp_name = os.path.splitext(target_file)[0]
        common.extract(decomp_name, download_dir)

        # move to target_dir
        src_dir = os.path.splitext(decomp_name)[0]
        shutil.move(src_dir, extract_dir)
        return


    def _check_version(self, version, target):
        """
        check whether specified version is available or not
        """
        self._logger.info('start check available version')
        ########################################
        # check file exists or not 
        #
        if llvm_url.urls[version][target] == '':
            return False
        else:
            return True


    def _get_all_files(self, version):
        """
        download and extract all files
        """
        self._logger.info('download all files')
        download_dir = os.path.join(self._llvmenv_home, 'llvm_build', version, 'files')
        common.makedirs(download_dir)

        ########################################
        # llvm
        #
        self._logger.info('get llvm files')
        url = llvm_url.urls[version]['llvm']
        llvm = os.path.join(self._llvmenv_home, 'llvm_build', version, 'llvm')
        self._get_and_extract(url, download_dir, llvm)


        ########################################
        # clang
        #
        self._logger.info('get clang files')
        url = llvm_url.urls[version]['clang']
        clang = os.path.join(llvm, 'tools', 'clang')
        self._get_and_extract(url, download_dir, clang)

        ########################################
        # clang-tool-extra
        #
        if self._check_version(self._options.version, 'clang-extra'):
            self._logger.info('get clang-tools-extra files')
            url = llvm_url.urls[version]['clang-extra']
            clang_extra = os.path.join(llvm, 'tools', 'clang', 'tools', 'extra')
            self._get_and_extract(url, download_dir, clang_extra)

        ########################################
        # compiler-rt
        #
        self._logger.info('get compiler-rt files')
        url = llvm_url.urls[version]['compiler-rt']
        compiler_rt = os.path.join(llvm, 'projects', 'compiler-rt')
        self._get_and_extract(url, download_dir, compiler_rt)

        ########################################
        # libcxx
        #
        if self._options.with_libcxx == True:
            self._logger.info('get libcxx files')
            url = llvm_url.urls[version]['libcxx']
            libcxx  = os.path.join(llvm, 'projects', 'libcxx')
            self._get_and_extract(url, download_dir, libcxx)

        ########################################
        # libcxxabi
        #
        if self._options.with_libcxxabi == True:
            self._logger.info('get libcxxabi files')
            url = llvm_url.urls[version]['libcxxabi']
            libcxxabi  = os.path.join(llvm, 'projects', 'libcxxabi')
            self._get_and_extract(url, download_dir, libcxxabi)


    def _configure(self, generator, builder, version):
        """
        exec configure
        """
        self._logger.info('start configure')
        build_dir =  os.path.join(self._llvmenv_home, 'llvm_build', version, 'build')

        ########################################
        # change directory
        #
        os.chdir(build_dir)

        ########################################
        # create cmd
        #
        cmd = [ os.path.join(self._llvmenv_home, 'llvm_build', version, 'llvm', 'configure' )]
        if generator == 'cmake':
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
        #if self._options.opt != '':
        #    opts = self._options.opt.split(' ')
        install_dir = os.path.join(self._llvmenv_home, 'llvms', version)
        if generator == 'cmake':
            for opt in opts:
                if opt.startswith('-DCMAKE_INSTALL_PREFIX') :
                    opts.remove(opt)

            opt_map = self._llvm_opts['cmake']
            copt_map = self._clang_opts['cmake']
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

            opt_map = _llvm_opts['autotools']
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
        # delete file dir
        #
        file_dir = os.path.join(self._llvmenv_home, 'llvm_build', version , 'files')
        common.remove_dir(file_dir)

        ########################################
        # if delete-src is True, delete src dir
        #
        src_dir = os.path.join(self._llvmenv_home, 'llvm_build', version , 'llvm')
        if self._options.delete_src == True:
            common.remove_dir(src_dir)

        ########################################
        # if delete-build is True, delete build
        #
        build_dir = os.path.join(self._llvmenv_home, 'llvm_build', version , 'build')
        if self._options.delete_build:
            common.remove_dir(build_dir)
        
        return

    def run(self):
        """
        run command
        """
        ret = True
        try:
            ########################################
            # check version
            #
            if not self._check_version(self._options.version, 'llvm'): 
                self._logger.error('%s is not available version' % self._options.version)
                return
            
            ########################################
            # check exists directory
            #
            install_dir = os.path.join(self._llvmenv_home , 'llvms' , self._options.version)
            if os.path.exists(install_dir):
                self._logger.error('directory %s already exists' % install_dir)
                self._logger.error('nothing to do')
                return

            build_base =  os.path.join(self._llvmenv_home , 'llvm_build' , self._options.version)
            if not os.path.exists( build_base ):
                os.makedirs(build_base) 

            build_dir =  os.path.join(build_base, 'build')
            if os.path.exists(build_dir):
                self._logger.warn('directory %s already exists' % build_dir)
                self._logger.warn('try to install from %s' % build_dir)
            else:
                ########################################
                # get files
                #
                src_dir =  os.path.join(self._llvmenv_home , 'llvm_build' , self._options.version , 'llvm')
                if not os.path.exists(src_dir):
                    self._get_all_files(self._options.version)
                os.makedirs(build_dir) 
                os.makedirs(install_dir) 
            
            ########################################
            # configure
            #
            self._configure(self._options.generator, self._options.builder, self._options.version)
            
            ########################################
            # make
            #
            self._make(self._options.builder, self._options.version)
            
            ########################################
            # make install
            #
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

