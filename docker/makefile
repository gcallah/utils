DOCKER_DIR = .
DH_ACCOUNT = gcallah
CONT_NAME = tandon-dev-env
REPO_URL = https://github.com/ep2572/curator.git
REPO_NAME = curator

FORCE:

test: FORCE
	echo "Does this run?"

dev_cont: FORCE
	docker build -t $(DH_ACCOUNT)/$(CONT_NAME) $(DOCKER_DIR) --build-arg repo=$(REPO_NAME) --build-arg repo_url=$(REPO_URL) -f $(DOCKER_DIR)/DevCont
	# don't push to DockerHub until all debugged!
	# docker push $(DH_ACCOUNT)/$(CONT_NAME):latest
