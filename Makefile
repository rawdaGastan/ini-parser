.PHONY: all test clean

deps:  ## Install dependencies
	pip install poetry
	poetry install

test: ## Run tests
	poetry run pytest -v test/test.py

doc: 
	pdoc --http localhost:8080 ini/parser.py