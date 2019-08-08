# Location of virtualenv used for development.
VENV?=.venv
VENV3?=.venv3
# Source virtualenv to execute command (flake8, sphinx, twine, etc...)
ACTIVATE_ENV = . $(VENV)/bin/activate

default: help


create-venv: ## create virtual env
	if [! -d $(VENV)]; then \
	    virtualenv $(VENV); && \
		exit
	fi

setup: ## setup a development virtualenv in current directory
	$(ACTIVATE_ENV) && \
		pip install --upgrade pip && \
		pip install -r requirements.txt

install: ## install into Python environment
	$(ACTIVATE_ENV) && \
		pip install -e .
.PHONY: install

init-db: ## initiate the database
	$(ACTIVATE_ENV) && \
		flask init-db
.PHONY: init-db	

run: ## run the server locally
	$(ACTIVATE_ENV) && \
		flask run
.PHONY: run

test: ## run the tests
	$(ACTIVATE_ENV) && \
		pip install -e . && \
		flake8 ptdk && \
		flake8 tests && \
		python -m pytest
.PHONY: test

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
