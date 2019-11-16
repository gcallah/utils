# Need to export as ENV var
export TEST_DIR = tests
export TEST_DATA = test_data
export CODE_DIR = ./source
export HTML_DIR = ./source/template
export REQUIREMENTS_DIR = .
PYLINT = flake8
PYLINTFLAGS =
PYTHONFILES = $(shell find source -name *.py)
PYTHONFILES += $(shell find tests -name *.py)

FORCE:

container: $(REQUIREMENTS_DIR)/Dockerfile  $(REQUIREMENTS_DIR)/requirements.txt
	docker build -t utils docker

pytests: FORCE
	$(LIB_DIR)/pytests.sh

tests: 

lint:
	$(PYLINT) $(PYTHONFILES)
	

prod: $(INCS) $(HTMLFILES) lint tests
	-git commit -a 
	git pull origin master
	git push origin master

local: $(INCS) $(HTMLFILES) lint tests
	-git commit -a
	git pull origin master
	git push origin master
