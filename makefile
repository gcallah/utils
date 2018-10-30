# Need to export as ENV var
export TEST_DIR = tests
export TEST_DATA = test_data
PYTHONFILES = $(shell ls *.py)

FORCE:

tests: FORCE
	$(TEST_DIR)/all_tests.sh

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	flake8 $*.py

repo: $(INCS) $(HTMLFILES) tests pylint
	-git commit -a 
	git pull origin master
	git push origin master
