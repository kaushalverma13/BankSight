# BankSight Makefile
# Common development tasks

.PHONY: help install test lint format clean docker

help:
	@echo "BankSight Development Commands"
	@echo "==============================="
	@echo "make install      - Install dependencies"
	@echo "make test         - Run tests"
	@echo "make lint         - Run linting checks"
	@echo "make format       - Format code with black"
	@echo "make clean        - Clean up generated files"
	@echo "make docker       - Build and run Docker containers"
	@echo "make run          - Run the application"
	@echo "make init         - Initialize the application"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/ --max-line-length=120
	pylint src/

format:
	black src/ tests/ *.py --line-length=120
	isort src/ tests/ *.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .coverage htmlcov
	rm -rf .mypy_cache

init:
	python init.py

run:
	streamlit run app.py

docker-build:
	docker build -t banksight:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f app

docker: docker-build docker-up

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

security-check:
	bandit -r src/
	safety check

type-check:
	mypy src/ --ignore-missing-imports

all: format lint test
