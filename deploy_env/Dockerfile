FROM python:3.9.6-slim-buster

RUN pip install "poetry>=1.2"

# Configuring poetry
RUN poetry config virtualenvs.create false
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean
# Copying requirements of a project
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src
RUN pip3 install setuptools

RUN pip install psycopg2-binary


# Installing requirements
RUN poetry install --no-root

# Copying actuall application
COPY . /app/src/
RUN poetry install

CMD ["/usr/local/bin/python", "-m", "foodshareapp"]