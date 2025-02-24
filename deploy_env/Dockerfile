FROM python:3.9.6-slim-buster

RUN pip install poetry==1.1.13

# Configuring poetry
RUN poetry config virtualenvs.create false
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean
# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src
RUN pip3 install setuptools



# Installing requirements
RUN poetry install

# Copying actuall application
COPY . /app/src/
RUN poetry install

CMD ["/usr/local/bin/python", "-m", "foodshareapp"]