FROM python:3.9.10-slim-bullseye

LABEL maintainer="rodrigo@eliseu.me"

ENV APP_DIR=/usr/src/app \
    APP_PORT=5000 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.11 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="${PATH}:/root/.local/bin"


RUN pip install pipx && python3 -m pipx ensurepath
RUN pipx install "poetry==$POETRY_VERSION"

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR ${APP_DIR}

RUN apt-get update && apt-get install -y \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    python-dev

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

COPY . .

EXPOSE ${APP_PORT}

CMD gunicorn --bind 0.0.0.0:${APP_PORT} --access-logfile - "better_roadmap.app:wsgi()"
