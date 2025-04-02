#!/bin/bash

. $KOUKOU_HOME/data_utils/common.sh

if [ -z $MONGO_USER ]
then
    export MONGO_USER=datamixmaster
fi

mongosh $CONNECT_STR --apiVersion 1 --username $MONGO_USER --password $MONGO_PASSWD
