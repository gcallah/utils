docker rm util_shell || true
docker run -it -p 8000:8000 --name util_shell -v $PWD:/home/utils gcallah/django:latest bash
