#!/usr/bin/env python
import logging
import os
import pytest
from subprocess import Popen, PIPE
import shutil
import subprocess
import unittest
home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libdir = os.path.join(home, 'src')

import sys
sys.path[0:0] = [
  libdir,
  ]
import llvmenv_main


class CommandTest(unittest.TestCase):
    def setUp(self):
        return

    def test_all_commands(self):
        """
        """
        os.environ['LLVMENV_HOME'] = llvmenv_home = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.test_home')
        os.environ['LLVMENV_ROOT'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.test_home')
        if os.path.exists(llvmenv_home):
            shutil.rmtree(llvmenv_home)

        sys.argv=['llvmenv', 'install', 'llvm_3.7', '--opt=-DCMAKE_CXX_COMPILER=clang++-3.6 -DCMAKE_C_COMPILER=clang-3.6']
        assert llvmenv_main.main() == True
        del logging.getLogger('llvmenv').handlers[:]

        sys.argv=['llvmenv', 'use', 'llvm_3.7']
        assert llvmenv_main.main() == True
        del logging.getLogger('llvmenv').handlers[:]

        sys.argv=['llvmenv', 'uninstall', 'llvm_3.7']
        assert llvmenv_main.main() == True

        # TODO: check more details...
        return

if __name__ == '__main__':
    pytest.main()
