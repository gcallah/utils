#!/bin/sh

cp ~/.vimrc .
cp ~/.vim/after/ftplugin/*.vim .

git commit .vimrc *.vim -m "Updating vim scripts."
git push origin master
