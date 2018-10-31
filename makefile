# Need to export as ENV var
export TEST_DIR = tests
export TEST_DATA = test_data
PYTHONFILES = $(shell ls *.py)
DOCKER_DIR = docker

FORCE:

container: $(DOCKER_DIR)/Dockerfile  $(DOCKER_DIR)/requirements.txt
	docker build -t utils docker

tests: FORCE
	$(TEST_DIR)/all_tests.sh

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	flake8 $*.py

repo: $(INCS) $(HTMLFILES) tests lint
	-git commit -a 
	git pull origin master
	git push origin master
