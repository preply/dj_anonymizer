.PHONY: help

help: ## Show help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

isort: ## run isort and change imports order
	isort dj_anonymizer example tests

isort_check_only: ## run isort and show diff
	isort -c dj_anonymizer example tests

flake8: ## run flake8
	flake8 .

test: ## run unittests
	DJANGO_SETTINGS_MODULE=tests.settings \
		python -m pytest $(scope)

coverage: ## run coverage
	DJANGO_SETTINGS_MODULE=tests.settings \
		python -m pytest --cov-report xml --cov=dj_anonymizer tests/

test_project: ## check if example project is working correctly - for dev env only
	cd example && python manage.py migrate && python manage.py anonymize_db

all: isort_check_only flake8 test test_project ## make all checks
