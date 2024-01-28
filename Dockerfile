FROM python:3.12-bullseye as builder

WORKDIR /opt/cookbook

ENV \
PIP_DISABLE_PIP_VERSION_CHECK="1" \
PIP_NO_CACHE_DIR="1"

RUN pip install poetry==1.7.0

ENV \
POETRY_NO_INTERACTION="1" \
POETRY_VIRTUALENVS_IN_PROJECT="1" \
POETRY_VIRTUALENVS_CREATE="1" \
POETRY_CACHE_DIR="/tmp/.poetry"

COPY poetry.lock pyproject.toml .
RUN \
--mount=type=cache,target=$POETRY_CACHE_DIR \
poetry install --only=main --no-interaction --no-ansi


FROM python:3.12-slim-bullseye as runtime

WORKDIR /opt/cookbook

ENV PATH="/opt/cookbook/.venv/bin:$PATH"

COPY --from=builder /opt/cookbook/.venv .venv
COPY cookbook .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "core.wsgi", "-b", "0.0.0.0:8000", "-w", "1"]
