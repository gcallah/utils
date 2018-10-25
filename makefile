# Need to export as ENV var
export TEST_DIR = tests
export TEST_DATA = test_data
PYTHONFILES = $(shell ls *.py)

FORCE:

tests: FORCE
	$(TEST_DIR)/all_tests.sh

pylint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	pylint -rn $*.py

repo: $(INCS) $(HTMLFILES) tests pylint
	-git commit -a 
	git pull origin master
	git push origin master
