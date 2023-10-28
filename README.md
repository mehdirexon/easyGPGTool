[![status: active](https://github.com/GIScience/badges/raw/master/status/active.svg)](https://github.com/GIScience/badges#active)

# 🔒 easyGPG Tool 🔒
## Table of Contents

* [Introduction](#introduction)

* [Features](#features)

* [Recently changes](#recently-changes)

* [How to use](#how-to-use)

* [Installation](#installation%EF%B8%8F)

* [Acknowledgements](#acknowledgements)

## Introduction👋

+ what is GPG?

GPG (GNU Privacy Guard) is a free and open-source tool for encrypting and signing data and communications. It uses public-key cryptography to ensure the security and privacy of your data. With GPG, you can encrypt your files and messages so that only the intended recipient can read them, and you can also digitally sign your messages to prove their authenticity.

+ what is easyGPG Tool

easyGPG Tool is a tool that allows you to work with GPG easily instead of using the original library.
This GUI version helps you to get rid of typing codes and other stuff. So you can easily do whatever just with forms. 🎉

## Features💡
Why use easyGPG Tool? 💻 

easyGPG makes it easy for anyone to use GPG for encryption and decryption without having to learn complex command-line codes. With its user-friendly interface, you can quickly and easily manage your keys and perform common tasks such as:

🔒 Encrypting your data to keep it safe from prying eyes

🔓 Decrypting your data quickly and easily whenever you need to access it

📤 Exporting your keys to a file for easy transfer between devices

📥 Importing keys from a file to quickly add them to your keychain

🔑 Generating a new key with just a few clicks or deleting an existing one if you no longer need it

📝 Keeping track of changes and updates with our detailed patch notes

🔍 Easily viewing all your keys in one place with our show keys feature

## Recently changes🆕
+ easyGPGTool has been added to pypi 
+ new run method has been added

## How to use📖
After using ```pip3 install easyGPGTool``` ,create a python file and follow these code:

```
from easyGPGTool.core import run
run()
```

# Note:

In the new version, installing on a local machine is being developed.

## Installation🛠️
### For Debian 
```
sudo apt update && sudo apt upgrade 
sudo apt install python3 && sudo apt install python3-pip 
pip3 install easyGPGTool
```
### For Fedora
```
sudo dnf update && sudo dnf upgrade 
sudo dnf install python3 && sudo dnf install python3-pip 
pip3 install easyGPGTool
```
### For Arch
```
sudo pacman -Syu
sudo pacman -S python python-pip
pip3 install easyGPGTool
```
### For MacOS
```
xcode-select --install
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
pip3 install easyGPGTool
```
### CentOS/RHEL
```
sudo yum update
sudo yum install python3 python3-pip
pip3 install easyGPGTool
```
### Gentoo
```
sudo emerge --sync && sudo emerge --update world 
sudo emerge --ask dev-lang/python dev-python/pip 
pip3 install easyGPGTool
```
### Slackware
```
slackpkg update && slackpkg upgrade-all 
slackpkg install python 
python -m ensurepip 
pip install --upgrade pip setuptools wheel 
pip install easyGPGTool
```
