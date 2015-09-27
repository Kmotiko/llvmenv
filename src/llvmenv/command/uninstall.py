from subprocess import Popen, PIPE 
import subprocess
import os

from llvmenv.lib import common

class UninstallSubcommand:
    def __init__(self, opts):
        self._logger=common.get_logger()
        self._options = opts


    def run(self):
        """
        run command
        """
        ########################################
        # get env and option
        #
        target_version = self._options.version
        llvmenv_home = os.getenv('LLVMENV_HOME')
        self._logger.info('uninstall version %s' % target_version)

        ########################################
        # check intalled version
        #
        installed = os.listdir(llvmenv_home + '/llvms/')
        if not target_version in installed:
            self._logger.error('%s is not installed yet' % target_version)
            return False

        ########################################
        # remove installed directory
        #
        self._logger.info('remove intalled directory of version %s' % target_version)
        common.remove_dir(os.path.join(llvmenv_home , 'llvms', target_version))

        ########################################
        # remove src directory
        #
        self._logger.info('remove src directory of version %s' % target_version)
        common.remove_dir(os.path.join(llvmenv_home , 'llvm_build', target_version, 'llvm'))
        
        ########################################
        # remove build directory
        #
        self._logger.info('remove build directory of version %s' % target_version)
        common.remove_dir(os.path.join(llvmenv_home , 'llvm_build', target_version))
        
        return True
