#!/bin/bash

_llvmenv_subcommand(){
    command=${COMP_WORDS[$COMP_CWORD]}
    COMPREPLY=( `compgen -W "init install uninstall use list" $command` ) 
}

_llvmenv_subcommands(){
    command=${COMP_WORDS[1]} 
    cur_word=${COMP_WORDS[$COMP_CWORD]}
    case $command in
        'install')
            _llvmenv_install $cur_word;;
        'uninstall')
            _llvmenv_uninstall $cur_word;;
        'init')
            ######################################
            # if arg num > 2  return
            #
            if [ $COMP_CWORD -gt 2 ]; then
                return
            fi
            _llvmenv_init $cur_word;;
        'use')
            ######################################
            # if arg num > 2  return
            #
            if [ $COMP_CWORD -gt 2 ]; then
                return
            fi
            _llvmenv_use $cur_word;;
        'list')
            ######################################
            # if arg num > 2  return
            #
            if [ $COMP_CWORD -gt 2 ]; then
                return
            fi
            _llvmenv_list $cur_word;;
    esac
}

_llvmenv_install(){
    opt_word=$1
    opt_len=${#opt_word}
    if [ -r "$LLVMENV_HOME/etc/available_versions" ]; then
        for line in `cat $LLVMENV_HOME/etc/available_versions`
        do
            install_versions="$line $install_versions"
        done
        COMPREPLY=( `compgen -W "$install_versions" -- $1` ) 
    else
        COMPREPLY=( `` ) 
    fi
}

_llvmenv_uninstall(){
    versions=`ls $LLVMENV_HOME/llvms`
    COMPREPLY=( `compgen -W "$versions" $1` ) 
}

_comp_word(){
    arg1=$1
    arg2=$2
    for i in `seq 1 ${#arg1}`
    do
        char_1=`echo $arg1|cut -b $i`
        char_2=`echo $arg2|cut -b $i`
        if [ $char_1 != $char_2  ]; then
            echo $i
            return
        fi
    done
    echo ${#arg1}
}

_llvmenv_init(){
    opt_word=$1
    opt_len=${#opt_word}
    COMPREPLY=( `compgen -W "--init --update" -- $1` )
}

_llvmenv_use(){
    versions=`ls $LLVMENV_HOME/llvms`
    COMPREPLY=( `compgen -W "$versions" $1` ) 
}

_llvmenv_list(){
    COMPREPLY=( `compgen -W "--all" -- $1` ) 
}

_llvmenv(){
    COMPREPLY=()

    if [ $COMP_CWORD -eq 1 ]; then
        _llvmenv_subcommand 
    elif [ $COMP_CWORD -ge 2 ]; then
        _llvmenv_subcommands 
    fi
}

complete -F _llvmenv llvmenv
