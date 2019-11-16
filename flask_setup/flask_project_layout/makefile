# Need to export as ENV var
export TEST_DIR = tests
export TEST_DATA = test_data
export CODE_DIR = .
export HTML_DIR = .
export DATA_DIR = $(CODE_DIR)/data
export REQUIREMENTS_DIR = requirements
PYTHONFILES = $(cd source && shell ls *.py)
PSHELL_SCRIPTS = $(shell ls *.sh | sed -e 's/.sh/.ps1/')
PSHELL_SCRIPTS += $(shell ls $(TEST_DIR)/*.sh | sed -e 's/.sh/.ps1/')
BASH2PS = python bash_to_powershell.py

FORCE:

container: $(REQUIREMENTS_DIR)/Dockerfile  $(REQUIREMENTS_DIR)/requirements.txt
	docker build -t utils docker

html_tests: FORCE
	$(TEST_DIR)/html_tests.sh

script_tests: FORCE
	$(TEST_DIR)/script_tests.sh

pytests: FORCE
	$(LIB_DIR)/pytests.sh

tests: html_tests script_tests

# download make for windows to run tests on powershell:
# http://gnuwin32.sourceforge.net/packages/make.htm

# the test can depend upon the ps1 files being built like this:
# pshell_html_tests: $(TEST_DIR)/html_tests_powershell.ps1

pshell_html_tests: FORCE
	$(info )
	python bash_to_powershell.py ./tests/html_tests.sh -d=True
	powershell -ExecutionPolicy ByPass $(TEST_DIR)/html_tests_powershell.ps1

%.ps1: %.sh
	$(BASH2PS) $<

pshell_scripts: $(PSHELL_SCRIPTS)

pshell_script_tests: FORCE
	$(info )
	python bash_to_powershell.py ./tests/script_tests.sh -d=True
	powershell -ExecutionPolicy ByPass $(TEST_DIR)/script_tests_powershell.ps1

pshell_tests: pshell_html_tests pshell_script_tests

lint: 
	flake8 $(PYTHONFILES)

prod: $(INCS) $(HTMLFILES) lint tests
	-git commit -a 
	git pull origin master
	git push origin master

local: $(INCS) $(HTMLFILES) lint tests
	-git commit -a
	git pull origin master
	git push origin master
