# A template makefile that works for static websites.
# Need to export TEMPLATE_DIR as ENV var
export TEMPLATE_DIR = templates
# Export MARKDOWN_DIR
export MARKDOWN_DIR = markdown_files
PTML_DIR = html_src
UTILS_DIR = utils
DOCKER_DIR = docker
# REPO = this repo!

INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/logo.txt $(TEMPLATE_DIR)/menu.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

MARKDOWN_FILES = $(shell ls $(MARKDOWN_DIR))

FORCE:

tests: FORCE
	echo "Here is where you should run your tests."

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $<
	# Optionally use render_md.awk to render makrdown files.(Requires Mistune)
#	$(UTILS_DIR)/render_md.awk <$< | $(UTILS_DIR)/html_include.awk >$@
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

local: $(HTMLFILES)

%.md: $(MARKDOWN_DIR)/%.md
	# Requires pandoc, uses commonmark flavor of markdown
	pandoc -f commonmark -t html5 <$< >$(PTML_DIR)/$@.ptml
	mv $(PTML_DIR)/$@.ptml $(PTML_DIR)/$$(basename -s .md $<).ptml

markdown: $(MARKDOWN_FILES)

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
