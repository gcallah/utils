export HOST_PORT="8000"
export REPO=curator
export REPO_PATH=/Users/gcallah/StudentRepos/curator
export CONT_NAME=tandon-dev-env
if [ $1 ]
then
    HOST_PORT=$1
fi

echo "Going to remove any lingering $CONT_NAME container."
docker rm $CONT_NAME 2> /dev/null || true
echo "Now running docker to spin up the container."
docker run -it -p $HOST_PORT:8000 -v $REPO_PATH:/home/$REPO gcallah/$CONT_NAME bash

