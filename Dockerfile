FROM --platform=linux/amd64 python:3.12-alpine3.18@sha256:dc2e8896e2bc0a52effa1249de614eee1b770a46cb1df25a72baf60a34ce5b1a AS alpine-amd64
FROM --platform=linux/arm64 python:3.12-alpine3.18@sha256:6bea708841800c7d17f384f982ad0168f66a24048b60a55262dc1d37f22073dc AS alpine-arm64

FROM alpine-$TARGETARCH AS python-base

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1

FROM python-base AS builder

RUN apk add --update python3-dev py3-pip build-base musl-dev libffi-dev openssl-dev cargo \
    && pip install --ignore-installed "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock /app/
RUN --mount=type=secret,id=credentials,required=true source /run/secrets/credentials \
    && POETRY_HTTP_BASIC_GITLAB_USERNAME=$GITLAB_USER POETRY_HTTP_BASIC_GITLAB_PASSWORD=$GITLAB_PASSWORD poetry install --only main --no-interaction --no-ansi --no-root

FROM builder AS dev

RUN poetry install --no-interaction --no-ansi --no-root
COPY . /app/

FROM python-base

ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /app/.venv /opt/venv
COPY . /app/

CMD ["./migrate_and_run.sh"]
