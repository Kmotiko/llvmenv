LLVMENV
==================

# はじめに
llvmenvはllvm/clangのインストール/管理を行うためのツールです。  
手元でバージョン切り替えて使うのが面倒だったので作ってみました。  
ほぼ個人用なので機能等はミニマムですが，最低限インストール/アンインストール/バージョンの切り替えは出きるはずです。　
Pythonで書いているので動作にはPythonが必要です。  

# 動作環境
以下の環境で動作確認しています。

|項目       |説明       |
|:----------|:----------|
|OS         | Ubuntu 13.04 64bit|
|Python     | Python 2.7|
|GCC        | GCC4.7.3|


# 使い方
使い方の説明を簡単に書いておきます。

## bashrc
$HOME/.bashrc を開いて以下を追記

```shell
export LLVMENV\_HOME=~/llvmenv
source $LLVMENV\_HOME/etc/llvmenvrc
```

## 初期化
最初に以下のコマンドで初期化します。

```shell
llvmenv init --init
```

実行するとsvn lsでリポジトリからLLVM,Clang,Compiler-rt,clang-extra-toolsのバージョン情報を取得します。  
ここで取得したバージョンをインストールコマンドでインストール対象として使用します。  

## リスト表示
以下のコマンドでinitで取得してきたインストール可能なバージョンを表示します。

```shell
llvmenv list --all
```

インストール済みのバージョンを表示する時は以下のコマンドを使用します。

```shell
llvmenv list
```

## インストール
LLVMをインストールしたいときは以下のコマンドを使用します。  
optに渡したオプションはそのままconfigureのオプションとして使用されます。  
ただしインストール先は内部で書き換えるのでprefixは指定しても無効になります。  

```shell
llvmenv install RELEASE_33 --no_delete_src_dir --no_delete_build_dir --opt="--enable-optimized"
```


## バージョン切り替え
使用するバージョンを切り替えには下記のコマンドを実行します。

```shell
llvmenv use RELEASE_33
```

## アンインストール
アンインストールする時は下記コマンドを実行します。

```shell
llvmenv uninstall RELEASE_33
```
