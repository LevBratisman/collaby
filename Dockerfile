FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && ln -s ~/.local/share/pypoetry/venv/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root

COPY . /app

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.run:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8002"]