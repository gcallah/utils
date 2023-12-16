#!/bin/bash

awk '{ print $1 }' api.datamixmaster.com.access.log.1 | sort -u | wc -l
