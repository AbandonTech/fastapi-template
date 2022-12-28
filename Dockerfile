FROM python:3.11-slim

RUN apt update -y \
    && apt install -y curl

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.2.2

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

ADD poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install

EXPOSE 8000

WORKDIR /app

ENTRYPOINT ["uvicorn"]
CMD ["run:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]