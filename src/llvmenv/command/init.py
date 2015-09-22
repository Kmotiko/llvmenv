import os
import re
from llvmenv.lib import common


class InitSubcommand():
    def __init__(self, opts):
        self.logger=common.get_logger()
        self.options = opts

    def run(self):
        """
        run command
        """
        try:
            self.__init()
            return True
        except Exception:
            return False

    def __init(self): 
        """
        exec initialize ... 
        """
        # self.logger.info( 'start initialize')

        #############################################
        # print export
        #
        self.__print_export_env()

        #############################################
        # print llvmenv_func
        #
        self.__print_llvmenv_func()

        #############################################
        # print completion
        #
        self.__print_complete_sh(llvmenv_home)
        return

    def __print_export_env(self):
        llvmenv_home = os.getenv('LLVMENV_HOME')
        home = os.getenv('HOME')
        if not llvmenv_home:
            llvmenv_home = os.path.join(home, '.llvmenv')
        print 'export PATH=\"%s:${PATH}\"' % os.path.join(llvmenv_home, 'links')
        return

    def __print_llvmenv_func(self):
        shell = os.getenv('SHELL')
        print 'llvmenv() {'
        print '  case $1 in'
        print '  use)'
        print '    command llvmenv \"$@\"'
        print '    exec \"%s\";;' % shell
        print '  *)'
        print '    command llvmenv \"$@\";;'
        print '  esac'
        print '}'
        return

    def __print_complete_sh(self, llvmenv_home):
        pattern = r"^.*bash.*"
        shell = os.getenv('SHELL')
        if re.match(pattern, shell) :
            completion = os.path.join(llvmenv_home, 'etc', 'bash_complete.d', 'complete.sh')
            print 'source %s' % completion
        return
