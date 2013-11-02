import os
from llvmenv.lib import common


class InitSubcommand():
    def __init__(self, opts):
        self.logger=common.get_logger()
        self.llvmenv_home = os.getenv('LLVMENV_HOME')
        self.options = opts

    def run(self):
        """
        run command
        """
        if self.options.init == True:
            self.init()
            return
        elif self.options.update == True:
            self.update()
            return
        else:
            self.logger.error('unknown command')
        return

    def init(self): 
        """
        exec initialize ... 
        """
        self.logger.info( 'start initialize version list')
        self.get_list()
        return

    def update(self):
        """
        exec update ... 
        """
        self.logger.info( 'start update version list')
        self.get_list()
        return

    def get_list(self): 
        """
        check release version and output it
        """
        self.logger.info( 'check available release version')

        llvmenv_home = os.getenv('LLVMENV_HOME')
        master = os.path.join(llvmenv_home, 'llvm_build', 'master')

        ########################################
        # check llvm tags
        #
        cmd = ['svn', 'ls']
        args = ['http://llvm.org/svn/llvm-project/llvm/tags']
        ret, llvm_out = common.exec_command(cmd + args)
        if ret == False:
            self.logger.error(out)
            return ret

        ########################################
        # check clang tags
        #
        cmd = ['svn', 'ls']
        args = ['http://llvm.org/svn/llvm-project/cfe/tags']
        ret, clang_out = common.exec_command(cmd + args)
        if ret == False:
            self.logger.error(out)
            return ret
        
        ########################################
        # check compiler-rt tags
        #
        cmd = ['svn', 'ls']
        args = ['http://llvm.org/svn/llvm-project/compiler-rt/tags']
        ret, compiler_rt_out = common.exec_command(cmd + args)
        if ret == False:
            self.logger.error(out)
            return ret
        

        ########################################
        # output available release branches
        #
        file_path =  os.path.join(llvmenv_home , 'etc','available_versions')
        list_file = open(file_path, 'w')
        list_file.write('trunk\n')
        #releases = [ x for x in llvm_out.split('\n') if x in clang_out.split('\n') and x in compiler_rt_out.split('\n') and x in extra_out.split('\n')]
        releases = [ x for x in llvm_out.split('\n') if x in clang_out.split('\n') and x in compiler_rt_out.split('\n')]
        for line in releases:
            split_line = line.split('/')

            ########################################
            # output to file
            #
            list_file.write(split_line[0]+ '\n')
        
        ########################################
        # check clang-tools-extra tags
        #
        file_path =  os.path.join(llvmenv_home , 'etc','clang_extra_versions')
        list_file = open(file_path, 'w')
        list_file.write('trunk\n')
        cmd = ['svn', 'ls']
        args = ['http://llvm.org/svn/llvm-project/clang-tools-extra/tags']
        ret, extra_out = common.exec_command(cmd + args)
        if ret == False:
            self.logger.error(out)
            return ret
        
        for line in extra_out.split('\n'):
            split_line = line.split('/')

            ########################################
            # output to file
            #
            list_file.write(split_line[0] + '\n')
        
        
        
        list_file.close()
        self.logger.info( 'save available version list')

        return
