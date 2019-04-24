# Need to export as ENV var
export TEST_DIR = tests
export TEST_DATA = test_data
export LIB_DIR = pylib
export CODE_DIR = .
export HTML_DIR = .
export DATA_DIR = $(CODE_DIR)/data
export DOCKER_DIR = docker
PYTHONFILES = $(shell ls *.py)
PYTHONFILES += $(shell ls $(LIB_DIR)/*.py)

FORCE:

container: $(DOCKER_DIR)/Dockerfile  $(DOCKER_DIR)/requirements.txt
	docker build -t utils docker

html_tests: FORCE
	$(TEST_DIR)/html_tests.sh

script_tests: FORCE
	$(TEST_DIR)/script_tests.sh

tests: html_tests script_tests

powershell_html_tests: FORCE
	powershell -ExecutionPolicy ByPass $(TEST_DIR)/html_tests_powershell.ps1

powershell_script_tests: FORCE
	powershell -ExecutionPolicy ByPass $(TEST_DIR)/script_tests_powershell.ps1

powershell_tests: powershell_html_tests powershell_script_tests

lint: 
	flake8 $(PYTHONFILES)

prod: $(INCS) $(HTMLFILES) lint tests
	-git commit -a 
	git pull origin master
	git push origin master
