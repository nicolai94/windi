FROM python:3.12

WORKDIR /app

# Установим poetry
ENV POETRY_HOME="/root/.local" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PATH="/root/.local/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

RUN chmod +x /app/start.sh