LLVMENV
==================

# What is this?
LLVMENV is support tool to install llvm/clang in your environment.  
Current features is minimum, but install and uninstall command will work well.  
This tool is written with python.  

# Environments

|項目       |Value       |
|:----------|:----------|
|OS         | Ubuntu 14.04 64bit|
|Python     | Python 2.7|
|GCC        | GCC 4.7.3|


# Initial setting

## get llvmenv
Cloning llvmenv code from github repository.

```
$ git clone https://github.com/Kmotiko/llvmenv.git $HOME/.llvmenv
```

## bashrc
To use llvmenv, please add following settings to $HOME/.bashrc.

```shell
export LLVMENV_HOME=~/.llvmenv
source $LLVMENV_HOME/etc/llvmenvrc
```


# How to use

LLVMENV has following sub-commands.

 * init
 * list
 * install
 * use
 * uninstall

We describe how to use sub-commands in this clause.

## Initialize
At first, initialize llvm information with following command.

```shell
llvmenv init --init
```

When running "init" command, this tool get version information about LLVM/Clang/Compiler-rt/Clang-extra-tools using "svn ls" command.  
You will be able to specify that version when execute install command.  


## List
The "list --all" command show available version to install.

```shell
llvmenv list --all
```

And more, "list" command show versions already installed.

```shell
llvmenv list
```

## Install
You can install llvm/clang with "install" subcommand.  
If you specify options with "--opt" option, that parameter is used as configure parameter except prefix.  
But, install target directory is defined in llvmenv, so prefix option is ignored whenever you specify it with "--opt".  

```shell
llvmenv install RELEASE_361.final --delete-src --delete-build --opt="--enable-optimized"
```

### Options

The install sub-command has options described in bellow.

|option                     | describe                                                            | default       |
|:--------------------------|:--------------------------------------------------------------------|:--------------|
|delete-src                 | delete src directory after install                                  | True          |
|delete-build               | delete build directory after install                                | True          |
|generator                  | specify generator: gnu or cmake                                     | gnu autotools |
|opt                        | this parameter will be told  to configure or cmake command as options       | -             |
|builder                    | specify builder: make or ninja                                      | make          |
|use-libcxx                 | set to use-libcxx                                                   | False         |
|use-libcxxabi              | set to use-libcxxabi                                                | False         |


## Use
The "use" sub-command enable specified llvm/clang version to use.


```shell
llvmenv use RELEASE_361.final
```

## Uninstall
You can uninstall llvm/clang with following command.

```shell
llvmenv uninstall RELEASE_361.final
```


# License

This software is distributed with MIT license.

```
Copyright (c) 2013 Kmotiko
```
