#!/bin/sh

echo "Please remove the damaged submodule using the editor"
vi .gitmodules
git add .gitmodules

echo "Remove submodule from the following file"
vi .git/config
git rm --cached $1
rm -rf .git/modules/$1
git commit -m "Remove submodules $1"
rm -rf $1
git push origin master

echo "Re-add Submodule"
git submodule add <submod_url>
