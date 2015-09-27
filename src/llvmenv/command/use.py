import os
import re
from llvmenv.lib import common

class UseSubcommand():
    def __init__(self, opts):
        self._logger=common.get_logger()
        self._llvmenv_home = os.getenv('LLVMENV_HOME')
        self._options = opts

    def run(self):
        """
        run command
        """
        use_version = self._options.version
        self._logger.info('enable version %s' % use_version)

        ########################################
        # check intalled version
        #
        installed = os.listdir(self._llvmenv_home + '/llvms/')
        if not use_version in installed:
            self._logger.error('%s is not installed yet' % use_version)
            return False
        
        ########################################
        # update rc file
        #
        self._update_version(use_version)

        ########################################
        # create sim link
        #
        self._create_link(use_version, self._options.suffix)
        return True

    def _update_version(self, version):
        """
        update using version of rc file
        """
        ########################################
        #
        #
        version_file = os.path.join(self._llvmenv_home, 'etc', 'version')
        with open(version_file, 'w') as f:
            f.write('%s' % version)
        return

    def _create_link(self, version, suffix=''):
        """
        create sim link
        """
        ########################################
        # create dir
        #
        dir_path = self._llvmenv_home + '/links'
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                os.remove(dir_path + '/' + file)
        else:
            os.mkdir(dir_path)
        
        ########################################
        # create sim link
        #
        os.chdir(dir_path)
        bin_path = self._llvmenv_home + '/llvms/' + version + '/bin/'
        for command in os.listdir(bin_path):
            cmd = ['ln', '-s', bin_path + command, command + suffix]
            common.exec_command(cmd)
        return
