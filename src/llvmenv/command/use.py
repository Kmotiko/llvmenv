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
            return False
        
        ########################################
        # update rc file
        #
        self.update_version(use_version)

        ########################################
        # create sim link
        #
        self.create_link(use_version, self.options.suffix)
        return True

    def update_version(self, version):
        """
        update using version of rc file
        """
        ########################################
        #
        #
        version_file = os.path.join(self.llvmenv_home, 'etc', 'version')
        with open(version_file, 'w') as f:
            f.write('%s' % version)
        return

    def create_link(self, version, suffix=''):
        """
        create sim link
        """
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
            cmd = ['ln', '-s', bin_path + command, command + suffix]
            common.exec_command(cmd)
        return
