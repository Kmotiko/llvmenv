import os
import re
from llvmenv.lib import common

class UseSubcommand():
    def __init__(self, opts):
        self.logger=common.get_logger()
        self.llvmenv_home = os.getenv('LLVMENV_HOME')
        self.options = opts

    def run(self):
        """
        run command
        """
        use_version = self.options.version
        self.logger.info('enable version %s' % use_version)

        ########################################
        # check intalled version
        #
        installed = os.listdir(self.llvmenv_home + '/llvms/')
        if not use_version in installed:
            self.logger.error('%s is not installed yet' % use_version)
            return
        
        ########################################
        # update rc file
        #
        self.update_version(use_version)

        ########################################
        # create sim link
        #
        self.create_link(use_version)
        return

    def update_version(self, version):
        """
        update using version of rc file
        """
        ########################################
        #
        #
        rcfile = self.llvmenv_home + '/etc/llvmenvrc'
        new_line = '\LLVMENV_LLVM_VERSION=' + self.llvmenv_home + '/llvms/' + version + '/bin/'
        cmd = ['sed']
        cmd += ['-i', '/^LLVMENV_LLVM_VERSION*/c %s ' % new_line, rcfile]
        common.exec_command_with_call(cmd)
        return

    def create_link(self, version):
        """
        create sim link
        """
        ########################################
        # create suffix
        #
        suffix=''
        if version.startswith('RELEASE'):
            suffix=version.split('.')[0].split('_')[1]
        elif version.startswith('trunk'):
            suffix='trunk'
        elif version.startswith('google'):
            suffix='google'

        ########################################
        # create dir
        #
        dir_path = self.llvmenv_home + '/links'
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                os.remove(dir_path + '/' + file)
        else:
            os.mkdir(dir_path)
        
        ########################################
        # create sim link
        #
        os.chdir(dir_path)
        bin_path = self.llvmenv_home + '/llvms/' + version + '/bin/'
        for command in os.listdir(bin_path):
            cmd = ['ln', '-s', bin_path + command, command + '_' + suffix]
            common.exec_command(cmd)
        return
