# Need to export as ENV var
export TEST_DIR = tests
export TEST_DATA = test_data
LIB = pylib
PYTHONFILES = $(shell ls *.py)
PYTHONFILES += $(shell ls $(LIB)/*.py)
DOCKER_DIR = docker

FORCE:

container: $(DOCKER_DIR)/Dockerfile  $(DOCKER_DIR)/requirements.txt
	docker build -t utils docker

tests: FORCE
	$(TEST_DIR)/all_tests.sh

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.lint:
	flake8 $*.py

# lint should go here... but we're not quite ready
repo: $(INCS) $(HTMLFILES) tests 
	-git commit -a 
	git pull origin master
	git push origin master
