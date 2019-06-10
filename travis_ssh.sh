#!/bin/sh

# How to add an ssh key to Travis-CI.

if [[ -z "$1" || -z "$2" || -z "$3" || -z "$4" ]]
then
    echo "Usage: travis-ssh.sh [keyfile] [ssh_user] [deploy_host] [org or com]."
    exit 1
fi

key=~/.ssh/$1
user=$2
host=$3
org_or_com=$4

echo "Generating ssh key."
ssh-keygen -t rsa -b 2048 -C 'build@travis-ci.org' -f $key

echo "Registering key with Travis -- you may need to login to Travis first!"
echo "(For login, use 'travis login --com' [or --org if you are hosted on .org)"
travis login --$org_or_com
travis encrypt-file $key --add --$org_or_com -r $repo
git add $1.enc

echo "Deploying key to server host."
ssh-copy-id -i $key.pub $user@$host

echo "You may need to modify your .travis.yml file at this point."
