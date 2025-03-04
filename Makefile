docker:
	touch .env
	cp deploy_env/.dev.env .env
	docker-compose -f deploy_env/docker-compose.yml -f deploy_env/docker-compose.dev.yml --project-directory . up --build


.PHONY: docker-builder
dockerbuild:
	docker-compose -f deploy_env/docker-compose.yml --project-directory . up --build

.PHONY: poetry
poetry:
	poetry install
	poetry run python -m foodshareapp

.PHONY: pre-commit
pre-commit:
	pre-commit install

.PHONY: tests
docker-tests:
	touch .env
	docker-compose -f deploy_env/docker-compose.yml --project-directory . run --rm api pytest -vv .
	docker-compose -f deploy_env/docker-compose.yml --project-directory . down


.PHONY: check black flake8 mypy

# Run all checks
check: black flake8 mypy test

# Check code formatting with Black
black:
	@echo "Running Black..."
	poetry run black .

# Lint code with Flake8
flake8:
	@echo "Running Flake8..."
	poetry run flake8 .

# Run static type checks with Mypy
mypy:
	@echo "Running Mypy..."
	poetry run mypy .

# Run tests 
test:
	poetry run pytest ./foodshareapp/tests/


.PHONY: frontendbuild
fe-build:
	poetry shell
	cd client && npm run build
	touch .env
	cp deploy_env/.dev.env .env
	docker-compose -f deploy_env/docker-compose.yml --project-directory . run --rm api pytest -vv .
	docker-compose -f deploy_env/docker-compose.yml --project-directory . down
