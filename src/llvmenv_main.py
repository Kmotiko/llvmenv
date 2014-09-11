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

parser_init.add_argument('--init', action='store_true', default=False, help='initialize llvm version info')
parser_init.add_argument('--update', action='store_true', default=False, help='update llvm version info')


#######################################
# install options
#
parser_install = \
    subparsers.add_parser('install', help='install llvm/clang')
parser_install.add_argument('version', type=str, default='release_33', help='install version')    
parser_install.add_argument('--opt', type=str, default='', help='configure option')    
parser_install.add_argument('--no-delete-src-dir', action='store_true', default=False, help='don\'t delete checkout src after install')
parser_install.add_argument('--no-delete-build-dir', action='store_true', default=False, help='don\'t delete build directory after install')
parser_install.add_argument('--generator', type=str, default='gnu', help='specify generator. default is gnu autotools')
parser_install.add_argument('--builder', type=str, default='make', help='specify builder. default is make')


#######################################
# uninstall options
#
parser_uninstall = \
    subparsers.add_parser('uninstall', help='uninstall llvm/clang')
parser_uninstall.add_argument('version', type=str, default=None, help='uninstall version')    
parser_uninstall.add_argument('--no-delete-build-dir', action='store_true', default=False, help='uninstall version')    

#######################################
#
#
parser_use = \
    subparsers.add_parser('use', help='install llvm/clang')
parser_use.add_argument('version', type=str, default=None,  help='enable version')    


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
    common.init_logger(config.get('default', 'LOG_LEVEL'), os.path.join(llvmenv_home, 'llvmenv.log'))

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
