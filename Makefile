.PHONY: install test lint clean format type-check

install:
	pip install -e ".[dev]"

test:
	pytest -p pytest_mock -v

lint:
	ruff check . --fix

type-check:
	uv run pyright

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf dist

format:
	uv run ruff format .

# run inspector tool
run-dev:
	uv run mcp dev src/basic_memory/mcp/main.py
