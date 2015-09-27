import os
import re
from llvmenv.lib import common


class InitSubcommand():
    def __init__(self, opts):
        self._logger=common.get_logger()
        self._options = opts

    def run(self):
        """
        run command
        """
        try:
            self._init()
            return True
        except Exception:
            return False

    def _init(self): 
        """
        exec initialize ... 
        """

        #############################################
        # print export
        #
        self._print_export_env()

        #############################################
        # print llvmenv_func
        #
        self._print_llvmenv_func()

        #############################################
        # print completion
        #
        self._print_complete_sh(llvmenv_home)
        return

    def _print_export_env(self):
        llvmenv_home = os.getenv('LLVMENV_HOME')
        home = os.getenv('HOME')
        if not llvmenv_home:
            llvmenv_home = os.path.join(home, '.llvmenv')
        print 'export PATH=\"%s:${PATH}\"' % os.path.join(llvmenv_home, 'links')
        return

    def _print_llvmenv_func(self):
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

    def _print_complete_sh(self, llvmenv_home):
        pattern = r"^.*bash.*"
        shell = os.getenv('SHELL')
        if re.match(pattern, shell) :
            completion = os.path.join(llvmenv_home, 'etc', 'bash_complete.d', 'complete.sh')
            print 'source %s' % completion
        return
