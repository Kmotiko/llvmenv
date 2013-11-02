#!/usr/bin/env python
import os
from llvmenv.lib import common

class InstallSubcommand():
    def __init__(self, opts):
        self.logger=common.get_logger()
        self.llvmenv_home = os.getenv('LLVMENV_HOME')
        self.options = opts

    def run(self):
        """
        run command
        """
        try:
            ########################################
            # check version
            #
            self.check_version(self.options.version, 'available_versions')
            
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
            # checkout
            #
            src_dir =  os.path.join(self.llvmenv_home , 'llvm_build' , self.options.version , 'llvm')
            if not os.path.exists(src_dir):
                self.checkout_all(self.options.version)
            
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
            self.logger.error(e.__args__)
        finally:
            ########################################
            # clean up directory
            #
            self.clean_directory(self.options.version)
            return


    def check_version(self, version, check_file):
        """
        check whether specified version is available or not
        """
        self.logger.info('start check available version')
        file_path =  os.path.join(self.llvmenv_home, 'etc', check_file)
        ########################################
        # check file exists or not 
        #
        if os.path.exists(file_path) == False:
            return False
        
        ########################################
        # check version
        #
        for line in open(file_path):
            if version == line.rstrip():
                return True
        return False


    def checkout(self, repo_base, version, target_dir):
        """
        """
        self.logger.info('start check out')
        if version == 'trunk':
            repo = repo_base + version
        else:
            repo = repo_base + '/tags/' + version
            if self.has_final(repo):
                repo = repo + '/final'
        cmd = ['svn', 'co']
        args = []
        args.append(repo)
        args.append(target_dir)
        self.logger.info('start cloning from %s ...' % repo)
        ret, out = common.exec_command(cmd + args)
        
        if not ret:
            self.logger.error(out)
            raise Exception('failed to check out from %s' % repo)

        return True

    def checkout_all(self, version):
        """
        checkout specified version
        """
        self.logger.info('start check out all')
        ########################################
        # 
        #
        llvmenv_home = os.getenv('LLVMENV_HOME')
        if len(llvmenv_home) == 0:
            self.logger.error('env LLVMENV_HOME is not set')
            return False

        self.logger.info('set home directory ... %s' % llvmenv_home)

        ########################################
        # checkout llvm
        #
        repo_base = 'http://llvm.org/svn/llvm-project/llvm/'
        llvm = os.path.join(llvmenv_home, 'llvm_build', version , 'llvm')
        self.checkout(repo_base, version, llvm)

        ########################################
        # checkout clang
        #
        repo_base = 'http://llvm.org/svn/llvm-project/cfe/'
        clang = os.path.join(llvm, 'tools', 'clang')
        self.checkout(repo_base, version, clang)
        
        ########################################
        # checkout compiler-rt
        #
        repo_base = 'http://llvm.org/svn/llvm-project/compiler-rt/'
        compiler_rt = os.path.join(llvm, 'projects', 'compiler-rt')
        self.checkout(repo_base, version, compiler_rt)


        ########################################
        # clang-extra-tools
        #
        if self.check_version(version, 'clang_extra_versions'):
            repo_base = 'http://llvm.org/svn/llvm-project/clang-tools-extra/'
            extra = os.path.join(llvm, 'tools', 'clang', 'tools', 'extra')
            self.checkout(repo_base, version, extra)

        return

    def has_final(self, repo):
        """
        check specified release has final directory or not 
        """
        cmd = ['svn', 'ls']
        cmd.append(repo)
        ret, out = common.exec_command(cmd)
        if 'final/' in out.split('\n'):
            return True
        return False

    def configure(self, generator, builder, version):
        """
        exec configure
        """
        self.logger.info('start configure')
        build_dir =  self.llvmenv_home + '/llvm_build/' + version + '/build'

        ########################################
        # change directory
        #
        os.chdir(build_dir)

        ########################################
        #
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
        if self.options.opt != '':
            opts = self.options.opt.split(' ')
        install_dir = self.llvmenv_home + '/llvms/' + version
        if generator == 'cmake':
            for opt in opts:
                if opt.split("=")[0] == '-DCMAKE_INSTALL_PREFIX':
                    opts.remove(opt)
            #args.append('-DLLVM_BUILD_TESTS=ON')
            #args.append('-DLLVM_ENABLE_ASSERTIONS=ON')  #default OFF IF RELEASE
            #args.append('-DLLVM_BUILD_EXAMPLES=ON')     #default OFF
            #args.append('-DCLANG_BUILD_EXAMPLES=ON')    #default OFF
            opts.append('-DCMAKE_EXPORT_COMPILE_COMMANDS=ON') #default OFF
            opts.append('-DCMAKE_INSTALL_PREFIX=%s' % install_dir)
            return opts

        elif generator=='gnu':
            for opt in opts:
                if opt.split("=")[0] == '--prefix':
                    opts.remove(opt)
            opts.append('--prefix=%s' % install_dir)
            #args.append('--disable-optimized')             #default yes
            #args.append('--enable-assertions')             #default yes
            #args.append('--enable-debug-runtime')
            #args.append('--enable-debug-symbols')
            return opts
        return opts

    def make(self, builder, version):
        """
        exec make
        """
        self.logger.info('start build')
        ########################################
        # change directory
        #
        build_dir =  self.llvmenv_home + '/llvm_build/' + version + '/build'
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
        # if no-delete-src is False, delete src dir
        #
        src_dir = os.path.join(self.llvmenv_home, 'llvm_build', version , 'llvm')
        if not self.options.no_delete_src_dir:
            common.remove_dir(src_dir)

        ########################################
        # if no-delete-build is False, delete build
        #
        build_dir = os.path.join(self.llvmenv_home, 'llvm_build', version , 'build')
        if not self.options.no_delete_build_dir:
            common.remove_dir(build_dir)
        
        return
