
# Introduction
This is the hugo version of my personal website. It has been created by cloning the wowchemy starter-huto-academic [wowchemy-academic] and then adding my content, and making minor customizations (e.g. custom fonts). 

# Directory Structure
The directory structure is exactly as-per the starter academic website. I am mentioning the files/directories that include my content/customizations. 

* `.github/workflows`: The action file ci_hugo.yml builds the website, and publishes the result to the branch _gh-pages_ of the same repository.

* `_bibliography/`: This directory contains the bib files stored in 
  https://github.com/rsvaliveti/pubs. This repo is included as a git submodule
  (i.e. not a copy).
  
* `assets/media/`: Includes icon.png (generated by favicon.io)

* `config/_default/`: 
	* `config.yaml`: contains the base URL
	* `menu.yaml`: Defines the items included in the menu
	* `params.yaml`:  The main change from the starter site is the selection of custom fonts

* `content/`:
	* `authors/admin/`:
		* _index.md: contains my short bio displayed on the home page.
		* avatar.jpg - my picture shown in the left column of the home page.
	* `home/`: I have kept my home page very simple. It shows my biography and contains a 
	   few links that can be used to contact me.
	* `education/`:
	   * `index.j2`: this file is the jinja2 template used to derive the index.md 
	     containing my educational experience & awards.
	   * `index.md`: This auto-generated page lists my education & awards
	* `work/`: 
	   * `index.j2`: this file is the jinja2 template used to derive the index.md
	     containing my work experience
	   * `index.md`: This auto-generated page lists the various industry positions I
	     have held.
	* `papers/`: lists the journal articles & conference papers. 
	  This page offers a filtered view of the publications
	  contained in the directory `publication/`.
	* `patents/`: lists my patents. This page offers a filtered view of the publications
	  contained in the directory `publication/`.
	* `publication/`: Contains autogenerated bibliography entries extracted from the two bib files: patents, publications. 
* `data/`:
	* `cv/cv.yaml`: My resume
	* `fonts/custom.yaml`: Loads the specfic Google fonts
	* `themes/custom.yaml`: Defines color choices for the theme. Unchanged from the starter version.
* `go.mod`, `go.sum`: Refer to the specific versions of wowchemy, wowchemy-cms
* `static/`:
	* `uploads`: Contains my resume
* `Makefile`: Contains the following targets:
	* bib: Process the bib files to generate the entries in content/publication.
	* serve: Build the site and serve it (at localhost:1313)
	* clean: Remove all auto-generated content

# References
[wowchemy-academic] https://github.com/wowchemy/starter-hugo-academic



