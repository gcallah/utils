DOCKER_DIR = .
DH_ACCOUNT = gcallah
CONT_NAME = tandon-dev-env
REPO_URL = https://github.com/ep2572/curator.git
REPO_NAME = curator
REQ_FILE = req-dev.txt
IMAGE_NAME = DevImage

FORCE:

test: FORCE
	echo "Does this run?"

dev_image: FORCE
	docker build -t $(DH_ACCOUNT)/$(CONT_NAME) $(DOCKER_DIR) --build-arg repo=$(REPO_NAME) --build-arg req_file=$(REQ_FILE) -f $(DOCKER_DIR)/$(IMAGE_NAME)
	# don't push to DockerHub until all debugged!
	# docker push $(DH_ACCOUNT)/$(CONT_NAME):latest
