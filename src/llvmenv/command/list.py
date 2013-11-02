import os
from llvmenv.lib import common

class ListSubcommand():
    def __init__(self, opts):
        self.logger=common.get_logger()
        self.llvmenv_home = os.getenv('LLVMENV_HOME')
        self.options = opts

    def run(self):
        """
        run command
        """
        ########################################
        # if specify all
        #
        if self.options.all == True:
            return self.list_available()
        else:
            return self.list_installed()

    def list_available(self):
        """
        output available version
        """
        file_path =  self.llvmenv_home + '/etc/available_versions'

        ########################################
        # check file exists or not 
        #
        if os.path.exists(file_path) == False:
            return False
        
        ########################################
        # print out list
        # 
        for line in open(file_path):
            print line.rstrip()
        return True

    def list_installed(self):
        """
        output installed version
        """
        ########################################
        #
        #
        dir_path =  self.llvmenv_home + '/llvms/'
        for version in os.listdir(dir_path):
            print version
        return True
