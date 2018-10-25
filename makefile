# Need to export as ENV var
export TEST_DIR = tests
export TEST_DATA = test_data
PYFILES = $(shell ls *.py)

FORCE:

tests: FORCE
	$(TEST_DIR)/all_tests.sh

repo: $(INCS) $(HTMLFILES) tests
	-git commit -a 
	git pull origin master
	git push origin master

