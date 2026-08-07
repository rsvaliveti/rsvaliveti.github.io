# Makefile for the Zola personal website.
# The `bib` target needs `uv`; `build`/`serve` need only the `zola` binary.

.DEFAULT_GOAL := help

.PHONY: env
env: ## Create the Python env used by the BibTeX importer
	uv sync

.PHONY: bib
bib: ## Regenerate publication/patent bundles from data/*.bib
	uv run scripts/import_bibtex.py data/papers.bib content/publications --overwrite
	uv run scripts/import_bibtex.py data/patents.bib content/patents --overwrite

.PHONY: clean_bib
clean_bib: ## Remove generated bundles from publications/ and patents/ (Ubuntu/Mac; keeps _index.md)
	find content/publications content/patents -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +

.PHONY: clean_bib_win
clean_bib_win: ## Remove generated bundles from publications/ and patents/ (Windows; keeps _index.md)
	powershell -NoProfile -Command "Get-ChildItem content/publications,content/patents -Directory | Remove-Item -Recurse -Force"

.PHONY: pp_script
pp_script: ## Pretty-print the importer script with ruff
	uvx ruff format scripts/import_bibtex.py

.PHONY: build
build: ## Build the static site into public/
	zola build

.PHONY: serve
serve: ## Serve the site locally with live reload
	zola serve

.PHONY: check
check: ## Validate the site without writing output
	zola check

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'
