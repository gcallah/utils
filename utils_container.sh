#!/bin/sh
echo "Going to remove any lingering utils container."
docker rm utils 2> /dev/null || true
echo "Now running docker to spin up the container."
docker run -it -v $PWD:/home/utils utils bash
