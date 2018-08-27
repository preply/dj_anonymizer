.PHONY: help

help: ## Show help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

isort: ## run isort with changing imports
	isort -rc dj_anonymizer example tests

isort_check_only: ## run isort only for check
	isort -rc -c dj_anonymizer example tests

flake8: ## run flake8
	flake8 .

test: ## run unittests
	DJANGO_SETTINGS_MODULE=tests.settings \
		python -m pytest

all: isort_check_only flake8 test ## make all checks
