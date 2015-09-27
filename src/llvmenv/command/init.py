import json
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
        if self._options.update_version :
            self._logger.info( 'start initialize version list')
            try:
                self._get_list()
            except Exception, e:
                self._logger.info(type(e))
                return False
        else:
            try:
                self._print_script()
            except Exception, e:
                return False
        return True

    def _get_list(self): 
        """
        check release version and output it
        """
        self._logger.info( 'check available release version')

        llvmenv_home = os.getenv('LLVMENV_HOME')
        llvm_base_url = 'http://llvm.org/svn/llvm-project/llvm/tags'
        clang_base_url = 'http://llvm.org/svn/llvm-project/cfe/tags'
        extra_base_url = 'http://llvm.org/svn/llvm-project/clang-tools-extra/tags'
        compiler_rt_base_url = 'http://llvm.org/svn/llvm-project/compiler-rt/tags'
        libcxx_base_url = 'http://llvm.org/svn/llvm-project/libcxx/tags'
        libcxxabi_base_url = 'http://llvm.org/svn/llvm-project/libcxxabi/tags'

        ########################################
        # check llvm tags
        #
        cmd = ['svn', 'ls']
        args = [llvm_base_url]
        ret, llvm_out = common.exec_command(cmd + args)
        if ret == False:
            self._logger.error(llvm_out)
            return ret

        ########################################
        # check clang tags
        #
        cmd = ['svn', 'ls']
        args = [clang_base_url]
        ret, clang_out = common.exec_command(cmd + args)
        if ret == False:
            self._logger.error(clang_out)
            return ret
        
        ########################################
        # check compiler-rt tags
        #
        cmd = ['svn', 'ls']
        args = [compiler_rt_base_url]
        ret, compiler_rt_out = common.exec_command(cmd + args)
        if ret == False:
            self._logger.error(compiler_rt_out)
            return ret

        def check_sub_dir(base_url, directories, ignore = ''):
            ver_map = {}
            for x in directories:
                ver_map[x] = []
                cmd = ['svn', 'ls']
                args = [base_url + '/' + x]
                ret, out = common.exec_command(cmd + args)
                if ret == False:
                    self._logger.error(out)
                    continue
                for line in out.split('\n'):
                    split_line = line.split('/')
                    ver_map[x].append(split_line[0])
            return ver_map

        

        ########################################
        # output available release branches
        #
        llvm_releases = [ x.split('/')[0] for x in llvm_out.split('\n') if x in clang_out.split('\n') and x in compiler_rt_out.split('\n') and not x.startswith('Apple')]
        version_map = {
                'trunk':{
                    'llvm': 'http://llvm.org/svn/llvm-project/llvm/trunk',
                    'clang': 'http://llvm.org/svn/llvm-project/cfe/trunk',
                    'clang-extra': 'http://llvm.org/svn/llvm-project/clang-tools-extra/trunk',
                    'compiler-rt': 'http://llvm.org/svn/llvm-project/compiler-rt/trunk',
                    'libcxx': 'http://llvm.org/svn/llvm-project/libcxx/trunk',
                    'libcxxabi': 'http://llvm.org/svn/llvm-project/libcxxabi/trunk'
                }
            }


        ########################################
        #
        #
        llvm_versions = check_sub_dir(llvm_base_url, llvm_releases)
        for version in llvm_versions.keys():
            for sub_ver in llvm_versions[version]:
                version_map[version + '.' + sub_ver] = {}
                version_map[version + '.' + sub_ver]['llvm'] = llvm_base_url + '/' + version + '/' + sub_ver
                version_map[version + '.' + sub_ver]['clang'] = clang_base_url + '/' + version + '/' + sub_ver
                version_map[version + '.' + sub_ver]['clang-extra'] = ''
                version_map[version + '.' + sub_ver]['compiler-rt'] = compiler_rt_base_url + '/' + version + '/' + sub_ver
                version_map[version + '.' + sub_ver]['libcxx'] = ''
                version_map[version + '.' + sub_ver]['libcxxabi'] = ''


        ########################################
        # check clang-tools-extra tags
        #
        cmd = ['svn', 'ls']
        args = [extra_base_url]
        ret, extra_out = common.exec_command(cmd + args)
        if ret == False:
            self._logger.error(extra_out)
            return ret
        releases = [ x.split('/')[0] for x in extra_out.split('\n')]
        for version in releases:
            for sub_ver in llvm_versions[version]:
                version_map[version + '.' + sub_ver]['clang-extra'] = extra_base_url + '/' + version + '/' + sub_ver
        

        ########################################
        # check libcxx tags
        #
        cmd = ['svn', 'ls']
        args = [libcxx_base_url]
        ret, libcxx_out = common.exec_command(cmd + args)
        if ret == False:
            self._logger.error(libcxx_out)
            return ret
        releases = [ x.split('/')[0] for x in libcxx_out.split('\n') if x.startswith('RELEASE')]
        for version in releases:
            for sub_ver in llvm_versions[version]:
                version_map[version + '.' + sub_ver]['libcxx'] = libcxx_base_url + '/' + version + '/' + sub_ver
        
        ########################################
        # check licxxabi tags
        #
        cmd = ['svn', 'ls']
        args = [libcxxabi_base_url]
        ret, libcxxabi_out = common.exec_command(cmd + args)
        if ret == False:
            self._logger.error(libcxxabi_out)
            return ret
        releases = [ x.split('/')[0] for x in libcxxabi_out.split('\n') if x.startswith('RELEASE')]
        for version in releases:
            for sub_ver in llvm_versions[version]:
                version_map[version + '.' + sub_ver]['libcxxabi'] = libcxxabi_base_url + '/' + version + '/' + sub_ver

        ########################################
        # output json
        #
        text = json.dumps(version_map, sort_keys=True, ensure_ascii=False, indent=2)
        if(not os.path.exists(os.path.join(llvmenv_home, 'etc'))):
            os.makedirs(os.path.join(llvmenv_home, 'etc'))
        with open(os.path.join(llvmenv_home, 'etc', 'versions'), 'w') as f:
            f.write(text.encode('utf-8'))
        self._logger.info( 'save available version list')
        return True

    def _print_script(self):
        llvmenv_home = os.getenv('LLVMENV_HOME')
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
