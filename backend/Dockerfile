FROM python:3.9-slim-buster as builder

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/opt/pysetup"

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl \
    gcc \
    openssl \
    libssl-dev \
    default-libmysqlclient-dev \
    mariadb-client \
    libmagic-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org/ | python -

COPY ./pyproject.toml /app/pyproject.toml
COPY ./app /app/
RUN mkdir -p /app/tmp && mkdir -p /app/image
RUN chmod +x /app/file.sh
WORKDIR /app
RUN poetry install --only main
