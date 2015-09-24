import os
import json
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
        file_path =  os.path.join(self.llvmenv_home, 'etc', 'versions')

        ########################################
        # check file exists or not 
        #
        if os.path.exists(file_path) == False:
            return False
        
        ########################################
        # print out list
        # 
        with open(file_path) as f:
            versions = json.loads(f.read(), encoding = 'utf-8')
            for version in sorted(versions.keys()):
                print version
        return True

    def list_installed(self):
        """
        output installed version
        """
        ########################################
        # get current llvm version
        #
        version_file = os.path.join(self.llvmenv_home, 'etc', 'version')
        current_version = ''
        with open(version_file, 'r') as f:
            current_version = f.read()

        ########################################
        # print version
        #
        dir_path =  self.llvmenv_home + '/llvms/'
        dir_path =  self.llvmenv_home + '/llvms/'
        for version in os.listdir(dir_path):
            if version.startswith('.') :
                continue
            elif version == current_version:
                print '* %s' % version
            else:
                print '  %s' % version
        return True
