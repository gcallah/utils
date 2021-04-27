export HOST_URL="127.0.0.1:8000"
export REPO=curator
export REPO_PATH=/Users/gcallah/StudentRepos/curator
export IMAGE_NAME=tandon-dev-env
if [ $1 ]
then
    HOST_PORT=$1
fi

echo "Going to remove any lingering $IMAGE_NAME container."
docker rm $IMAGE_NAME 2> /dev/null || true
echo "Now running docker to spin up the container."
docker run -it -p $HOST_PORT:8000 -v $REPO_PATH:/home/$REPO gcallah/$IMAGE_NAME bash

