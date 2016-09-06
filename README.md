LLVMENV
==================


# What is this?
LLVMENV is support tool to install llvm/clang in your environment.  
Current features is minimum, but install and uninstall command will work well.  
This tool is written with python.  

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
export PATH=$LLVMENV_HOME/bin:$PATH
if which llvmenv > /dev/null; then eval "$(llvmenv init)"; fi
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
llvmenv init --update-version
```

When running "init --update-version" command, llvmenv get version information about LLVM/Clang/Compiler-rt/LLDB/Clang-extra-tools using "svn ls" command.  
Now, you will be able to specify the version when execute install command.  


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
# DEBUG build
llvmenv install RELEASE_361.final --delete-src=false --delete-build=false --disable-optimized --enable-assertions=true
```

### Options

The install sub-command has options described in bellow.

|option                     | description                                                         | default       |
|:--------------------------|:--------------------------------------------------------------------|:--------------|
|delete-src                 | delete src directory after install                                  | True          |
|delete-build               | delete build directory after install                                | True          |
|generator                  | specify generator: gnu or cmake                                     | cmake         |
|enable-targets             | specify target architecture to build.                               | host          |
|disable-optimized          | If this option specify, LLVM/Clang's build-type is set to DEBUG. Otherwise, set to RELEASE.     | RELEASE |
|enable-assertions          | enable assertions or not                                            | -             |
|build-examples             | build llvm/clang examples                                           | -             |
|build-tests                | build llvm/clang tests                                              | -             |
|opt                        | This parameter will be directory told to configure or cmake command as options| -             |
|builder                    | specify builder: make or ninja                                      | ninja         |
|with-libcxx                | set to use libcxx                                                   | -             |
|with-libcxxabi             | set to use libcxxabi                                                | -             |
|with-lldb                  | set to use lldb                                                     | -             |


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
