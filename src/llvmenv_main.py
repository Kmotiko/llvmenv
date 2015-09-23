#!/usr/bin/env python
import argparse
import sys
from llvmenv.lib import downloader
from llvmenv.lib import common
from llvmenv.command import init 
from llvmenv.command  import use
from llvmenv.command import list
from llvmenv.command import install
from llvmenv.command import uninstall
import os

#######################################
#
#
parser = argparse.ArgumentParser(
        description='llvmenv manager',
        prog='llvmenv')
subparsers = parser.add_subparsers(help='subcommand')

#######################################
# init options
#
parser_init = \
    subparsers.add_parser('init', help='initialize llvmenv')

#######################################
# install options
#
str2bool = lambda opt_str:  False if opt_str == 'False' or opt_str == 'false' else True
parser_install = \
    subparsers.add_parser('install', help='install llvm/clang')
parser_install.add_argument('version', type=str, default='release_361.final', help='install target version')
parser_install.add_argument('--enable-targets', type=str, default='host', help='specify target to build. default is host')
parser_install.add_argument('--enable-optimized', type=str2bool, default='True', help='specify build type. RELEASE or DEBUG')
parser_install.add_argument('--enable-assertions', type=str2bool, default='False', help='enable assertions or not')
parser_install.add_argument('--build-examples', type=str2bool, default='True', help='build llvm examples or not')
parser_install.add_argument('--build-tests', type=str2bool, default='True', help='build llvm tests or not. This argument is available when using cmake.')
parser_install.add_argument('--opt', type=str, default='', help='configure option. You can use this field to specify configure option directory')
parser_install.add_argument('--delete-src', type=str2bool, default='True', help='delete checkout src after install')
parser_install.add_argument('--delete-build', type=str2bool, default='True', help='delete build directory after install')
parser_install.add_argument('--generator', type=str, default='cmake', help='specify generator. default is cmake')
parser_install.add_argument('--builder', type=str, default='ninja', help='specify builder. default is ninja')
parser_install.add_argument('--use-libcxx', action='store_true', default=False, help='use libcxx as the standard C++ Library')
parser_install.add_argument('--use-libcxxabi', action='store_true', default=False, help='use libcxxabi as the C++ ABI Library')


#######################################
# uninstall options
#
parser_uninstall = \
    subparsers.add_parser('uninstall', help='uninstall llvm/clang')
parser_uninstall.add_argument('version', type=str, default=None, help='uninstall version')

#######################################
#
#
parser_use = \
    subparsers.add_parser('use', help='install llvm/clang')
parser_use.add_argument('version', type=str, default=None,  help='enable version')
parser_use.add_argument('--suffix', type=str, default='', help='specify suffix')



#######################################
# list options
#
parser_list = \
    subparsers.add_parser('list', help='print llvm/clang version')
parser_list.add_argument('--all', action='store_true', default=False, help='print all available version')    



def main():
    #######################################
    # init logger and load config
    #
    llvmenv_home = os.getenv('LLVMENV_HOME')
    config=common.load_config(os.path.join(llvmenv_home, 'etc', 'llvmenv.conf'))
    common.init_logger(config.get('default', 'log_level'), os.path.join(llvmenv_home, 'llvmenv.log'))
    #config=common.load_yaml(os.path.join(llvmenv_home, 'etc', 'config.yml'))
    #common.init_logger(config['common']['log_level'], os.path.join(llvmenv_home, 'llvmenv.log'))

    #######################################
    # parse
    #
    options= parser.parse_args()
    subcommand = sys.argv[1]

    #######################################
    # init
    #
    if subcommand == 'init':
        command = init.InitSubcommand(options)

    #######################################
    # install
    #
    elif subcommand == 'install':
        command = install.InstallSubcommand(options)
    
    #######################################
    # uninstall
    #
    elif subcommand == 'uninstall':
        command = uninstall.UninstallSubcommand(options)
    
    #######################################
    # use
    #
    elif subcommand == 'use':
        command = use.UseSubcommand(options)

    #######################################
    # list
    #
    elif subcommand == 'list':
        command = list.ListSubcommand(options)
    
    return command.run()
