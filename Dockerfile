FROM python:3.10.12-bookworm

ENV PYTHONUNBUFFERED=1 POETRY_VERSION=1.6.1

ENV PATH="/root/.local/bin:$PATH"

RUN apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml /detector/

WORKDIR /detector

RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi

COPY . /detector
