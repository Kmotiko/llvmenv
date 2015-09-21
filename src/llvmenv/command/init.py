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
        self.init()
        return

    def init(self): 
        """
        exec initialize ... 
        """
        self.logger.info( 'start initialize version list')
        # TODO: initialize environment
        return
