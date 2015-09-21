#!/usr/bin/env python
import os
import llvm_url
import shutil
from llvmenv.lib import common

class InstallSubcommand():
    llvm_opts = {
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
    clang_opts = {
            "cmake":{
                "build_examples": {
                    "key": "-DCLANG_BUILD_EXAMPLES", 
                    True: "ON", 
                    False: "OFF"}
                }
            }


    def __init__(self, opts):
        self.logger=common.get_logger()
        self.llvmenv_home = os.getenv('LLVMENV_HOME')
        self.options = opts


    def __get_and_extract(self, url, download_dir = '/tmp/', extract_dir = '/tmp/'):
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


    def check_version(self, version, target):
        """
        check whether specified version is available or not
        """
        self.logger.info('start check available version')
        ########################################
        # check file exists or not 
        #
        if llvm_url.urls[version][target] == '':
            return False
        else:
            return True


    def get_all_files(self, version):
        """
        download and extract all files
        """
        self.logger.info('download all files')
        download_dir = os.path.join(self.llvmenv_home, 'llvm_build', version, 'files')
        common.makedirs(download_dir)

        ########################################
        # llvm
        #
        self.logger.info('get llvm files')
        url = llvm_url.urls[version]['llvm']
        llvm = os.path.join(self.llvmenv_home, 'llvm_build', version, 'llvm')
        self.__get_and_extract(url, download_dir, llvm)


        ########################################
        # clang
        #
        self.logger.info('get clang files')
        url = llvm_url.urls[version]['clang']
        clang = os.path.join(llvm, 'tools', 'clang')
        self.__get_and_extract(url, download_dir, clang)

        ########################################
        # clang-tool-extra
        #
        if self.check_version(self.options.version, 'clang-extra'):
            self.logger.info('get clang-tools-extra files')
            url = llvm_url.urls[version]['clang-extra']
            clang_extra = os.path.join(llvm, 'tools', 'clang', 'tools', 'extra')
            self.__get_and_extract(url, download_dir, clang_extra)

        ########################################
        # compiler-rt
        #
        self.logger.info('get compiler-rt files')
        url = llvm_url.urls[version]['compiler-rt']
        compiler_rt = os.path.join(llvm, 'projects', 'compiler-rt')
        self.__get_and_extract(url, download_dir, compiler_rt)

        ########################################
        # libcxx
        #
        if self.options.use_libcxx == True:
            self.logger.info('get libcxx files')
            url = llvm_url.urls[version]['libcxx']
            libcxx  = os.path.join(llvm, 'projects', 'libcxx')
            self.__get_and_extract(url, download_dir, libcxx)

        ########################################
        # libcxxabi
        #
        if self.options.use_libcxxabi == True:
            self.logger.info('get libcxxabi files')
            url = llvm_url.urls[version]['libcxxabi']
            libcxxabi  = os.path.join(llvm, 'projects', 'libcxxabi')
            self.__get_and_extract(url, download_dir, libcxxabi)


    def configure(self, generator, builder, version):
        """
        exec configure
        """
        self.logger.info('start configure')
        build_dir =  os.path.join(self.llvmenv_home, 'llvm_build', version, 'build')

        ########################################
        # change directory
        #
        os.chdir(build_dir)

        ########################################
        # create cmd
        #
        cmd = [ os.path.join(self.llvmenv_home, 'llvm_build', version, 'llvm', 'configure' )]
        if generator == 'cmake':
            cmd = [generator]
            if builder == 'ninja':
                cmd.append('-G')
                cmd.append('Ninja')
            cmd.append('../llvm')
        args = self.generate_opts(generator, version)
        self.logger.info('configure option is ... %s' % args)
        cmd += args
        if common.exec_command_with_call(cmd):
            raise Exception('failed to configure')
        return


    def generate_opts(self, generator, version):
        opts = []
        #if self.options.opt != '':
        #    opts = self.options.opt.split(' ')
        install_dir = os.path.join(self.llvmenv_home, 'llvms', version)
        if generator == 'cmake':
            for opt in opts:
                if opt.startswith('-DCMAKE_INSTALL_PREFIX') :
                    opts.remove(opt)

            opt_map = self.llvm_opts['cmake']
            copt_map = self.clang_opts['cmake']
            # enable_targets
            opt_str = '%s=%s' % (opt_map['enable_targets'], self.options.enable_targets)
            opts.append(opt_str)
            # build_type
            opt_str = '%s=%s' % (opt_map['enable_optimized']['key'], opt_map['enable_optimized'][self.options.enable_optimized])
            opts.append(opt_str)
            # enable_assertions
            opt_str = '%s=%s' % (opt_map['enable_assertions']['key'], opt_map['enable_assertions'][self.options.enable_assertions])
            opts.append(opt_str)
            # build_examples
            opt_str = '%s=%s' % (opt_map['build_examples']['key'], opt_map['build_examples'][self.options.build_examples])
            opts.append(opt_str)
            opt_str = '%s=%s' % (copt_map['build_examples']['key'], copt_map['build_examples'][self.options.build_examples])
            opts.append(opt_str)
            # build_tests
            opt_str = '%s=%s' % (opt_map['build_tests']['key'], opt_map['build_tests'][self.options.build_tests])
            opts.append(opt_str)
            opts.append('-DCMAKE_EXPORT_COMPILE_COMMANDS=ON') 
            opts.append('-DCMAKE_INSTALL_PREFIX=%s' % install_dir)

        elif generator=='autotools':
            for opt in opts:
                if opt.startswith('--prefix') :
                    opts.remove(opt)

            opt_map = llvm_opts['autotools']
            # enable_targets
            opt_str = '%s=%s' % (opt_map['enable_targets'], self.options.enable_targets)
            opts.append(opt_str)
            ## build_type
            opt_str = '%s' % (opt_map['enable_optimized'][self.options.enable_optimized])
            opts.append(opt_str)
            ## enable_assertions
            opt_str = '%s' % (opt_map['enable_assertions'][self.options.enable_optimized])
            opts.append(opt_str)
            opts.append('--prefix=%s' % install_dir)

        return opts

    def make(self, builder, version):
        """
        exec make
        """
        self.logger.info('start build')
        ########################################
        # change directory
        #
        build_dir =  os.path.join(self.llvmenv_home, 'llvm_build', version, 'build')
        os.chdir(build_dir)

        ########################################
        # do make
        #
        cmd = [builder]
        if common.exec_command_with_call(cmd):
            raise Exception('failed to configure')
        return

    def install(self, builder, version):
        """
        exec install
        """
        self.logger.info('start install')
        ########################################
        # change directory
        #
        build_dir =  self.llvmenv_home + '/llvm_build/' + version + '/build'
        os.chdir(build_dir)

        ########################################
        # do make install
        #
        cmd = [builder, 'install']
        if common.exec_command_with_call(cmd):
            raise Exception('failed to configure')
        return

    def clean_directory(self, version):
        self.logger.info('start clean directory')
        ########################################
        # delete file dir
        #
        file_dir = os.path.join(self.llvmenv_home, 'llvm_build', version , 'files')
        common.remove_dir(file_dir)

        ########################################
        # if delete-src is True, delete src dir
        #
        src_dir = os.path.join(self.llvmenv_home, 'llvm_build', version , 'llvm')
        if self.options.delete_src == True:
            common.remove_dir(src_dir)

        ########################################
        # if delete-build is True, delete build
        #
        build_dir = os.path.join(self.llvmenv_home, 'llvm_build', version , 'build')
        if self.options.delete_build:
            common.remove_dir(build_dir)
        
        return

    def run(self):
        """
        run command
        """
        try:
            ########################################
            # check version
            #
            if not self.check_version(self.options.version, 'llvm'): 
                self.logger.error('%s is not available version' % self.options.version)
                return
            
            ########################################
            # check exists directory
            #
            install_dir = os.path.join(self.llvmenv_home , 'llvms' , self.options.version)
            if os.path.exists(install_dir):
                self.logger.error('directory %s already exists' % install_dir)
                self.logger.error('nothing to do')
                return

            build_base =  os.path.join(self.llvmenv_home , 'llvm_build' , self.options.version)
            if not os.path.exists( build_base ):
                os.makedirs(build_base) 

            build_dir =  os.path.join(build_base, 'build')
            if os.path.exists(build_dir):
                self.logger.warn('directory %s already exists' % build_dir)
                self.logger.warn('try to install from %s' % build_dir)

                self.configure(self.options.generator, self.options.builder)
                self.make(self.options.builder)
                os.makedirs(install_dir) 
                self.install(self.options.builder)
                return 

            ########################################
            # get files
            #
            src_dir =  os.path.join(self.llvmenv_home , 'llvm_build' , self.options.version , 'llvm')
            if not os.path.exists(src_dir):
                self.get_all_files(self.options.version)
            
            ########################################
            # configure
            #
            os.makedirs(build_dir) 
            self.configure(self.options.generator, self.options.builder, self.options.version)
            
            ########################################
            # make
            #
            self.make(self.options.builder, self.options.version)
            
            ########################################
            # make install
            #
            os.makedirs(install_dir) 
            self.install(self.options.builder, self.options.version)

            return

        except Exception,e:
            self.logger.error(type(e))
            self.logger.error(e.__args__)

        finally:
            ########################################
            # clean up directory
            #
            self.clean_directory(self.options.version)
            return

