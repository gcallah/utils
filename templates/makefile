# A template makefile that works for static websites.
# Need to export TEMPLATE_DIR as ENV var
export TEMPLATE_DIR = templates
# Export MARKDOWN_DIR
export MARKDOWN_DIR = md
PTML_DIR = html_src
UTILS_DIR = utils
DOCKER_DIR = docker
# Change PANDOC if pandoc isn't in your PATH variable
# Or simply add pandoc to your PATH
PANDOC = pandoc
# REPO = this repo!

INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/logo.txt $(TEMPLATE_DIR)/menu.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/$(PTML_DIR)\///')

PTMLFILES = $(shell ls $(MARKDOWN_DIR)/*.md | sed -e 's/.md/.ptml/' | sed -e 's/$(MARKDOWN_DIR)/$(PTML_DIR)/')

FORCE:

tests: FORCE
	echo "Here is where you should run your tests."

%.html: $(PTML_DIR)/%.ptml $(PTMLFILES) $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $<
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

local: $(HTMLFILES) $(INCS)

$(PTML_DIR)/%.ptml: $(MARKDOWN_DIR)/%.md
	# Requires pandoc, uses commonmark flavor of markdown
	$(PANDOC) -f commonmark -t html5 <$< >$@

ptml: $(PTMLFILES)

prod: $(INCS) $(HTMLFILES) tests
	-git commit -a 
	git pull origin master
	git push origin master

submods:
	git submodule foreach 'git pull origin master'
	
nocrud:
	rm *~
	rm .*swp
	rm $(PTML_DIR)/*~
	rm $(PTML_DIR)/.*swp

clean:
	touch $(PTML_DIR)/*.ptml; make local
