.PHONY: docker
docker:
	touch .env
	docker-compose -f deploy_environments/docker-compose.yml -f deploy_environments/docker-compose.dev.yml --project-directory . up

.PHONY: docker-builder
dockerbuild:
	docker-compose -f deploy_environments/docker-compose.yml --project-directory . up --build

.PHONY: poetry
poetry:
	poetry install
	poetry run python -m foodshareapp_api

.PHONY: pre-commit
pre-commit:
	pre-commit install

.PHONY: tests
docker-tests:
	docker-compose -f deploy_environments/docker-compose.yml --project-directory . run --rm api pytest -vv .
	docker-compose -f deploy_environments/docker-compose.yml --project-directory . down


.PHONY: test
test:
	poetry run pytest ./prspcts_api/tests/

