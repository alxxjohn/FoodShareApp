# FoodShareApp

## Table of Contents

- [Installation](#installation)
  - [Makefile](#makefile)
  - [Poetry](#makefile)
  - [Docker](#docker)
- [Project structure](#project-structure)
- [Running tests](#running-tests)
- [Services](#services)
- [Contributors](#contributors)

## Installation

### Makefile

start services using makefile

```bash

make ['docker' or 'poetry']

```

below are the commands called via poetry or docker.

### Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m foodshareapp_api
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: <https://python-poetry.org/>

### Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy_environments/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy_environments/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f deploy_environments/docker-compose.yml -f deploy_environments/docker-compose.dev.yml --project-directory . up
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f deploy_environments/docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "foodshareapp"
foodshareapp_api
├── db  # module contains db configurations
    ├── migrations  # database migrations.
    └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services (redis etc).
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── app  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
        ├── router.py  # Main router.
    ├── utils  # Package with all handlers.
        └── app_exceptions.py  # exception handling.
        └── service_result.py 
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy_env/docker-compose.yml --project-directory . run --rm api pytest -vv .
docker-compose -f deploy_env/docker-compose.yml --project-directory . down
```

For running tests on your local machine.

1. you need to start a database.

I prefer doing it with docker:

```bash
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=foodshareapp_api" -e "POSTGRES_USER=foodshareapp_api" -e "POSTGRES_DB=foodshareapp_api" postgres:13.6-bullseye
```

2.Run the pytest.

```bash
pytest -vv .
```

## Services

```bash

api /8000

```

## Contributors

- Alex John
- Dillon Kilgallon
- Ine Park
- Kyle Cortez
