##
## file: Makefile
## description:
##   - This is the Makefile for genertating my personal website. 
## dependencies:
##   - go (language) & hugo-extended are installed on the system
##   - pdm (Python Dependency Manager) is installed on the system
##

#### PARAMETERS

PUBLISH=public/
P=1313
BIBDIR=_bibliography
CVDIR=data/cv
AUTHOR_DIR=content/authors/admin
VIRTUALENV = .venv

###
.PHONY:	about bib build build2 clean clean-all clean-venv default serve

default:	$(VIRTUALENV) build

# Build the virtual environment
$(VIRTUALENV):	pyproject.toml
	pdm install

# generate the contents/authots/admin/_index.md from cv.yaml
about:
	pdm run jinja -d $(CVDIR)/cv.yaml $(AUTHOR_DIR)/_index.j2 > $(AUTHOR_DIR)/_index.md

# generate the static HTML pages for the bibliography
bib: $(VIRTUALENV)
	# Import from BibTexfiles
	pdm run academic import --bibtex $(BIBDIR)/papers.bib content/publication
	pdm run academic import --bibtex $(BIBDIR)/patents.bib content/publication

# Build the website (basic)
build:	
	hugo --gc --minify

# Build the website (complete)
build2:	about bib build

clean:
	# Removing HTML directory: $(PUBLISH)
	@rm -rf $(PUBLISH)

clean-all:	clean
	# Removing publications directory
	@rm -rf content/publication

clean-venv:
	# Removing virtual environment dir: $(VIRTUALENV)
	rm -rf $(VIRTUALENV)

serve:
	hugo serve
