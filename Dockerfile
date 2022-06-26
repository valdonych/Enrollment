FROM python:3.9-slim


ENV POETRY_VERSION=1.1.5
ARG ENVIRONMENT=production

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get autoclean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*  \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

WORKDIR /opt/app

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry install $(if test "$ENVIRONMENT" = production; then echo "--no-dev"; fi)

COPY app app
COPY Makefile Makefile


CMD ["/sbin/init"]