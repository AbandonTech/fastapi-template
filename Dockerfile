FROM ghcr.io/owl-corp/python-poetry-base:3.11-slim

ADD poetry.lock pyproject.toml ./
RUN poetry install --no-root \
    && poetry run prisma generate

WORKDIR /app
ADD ./app ./app
ADD ./prisma ./prisma

EXPOSE 80

# Pull the uvicorn_extra build arg and ave it as an env var.
# The CMD instruction is ran at execution time, so it also needs to be an env var, so that it is available at that time.
ARG uvicorn_extras=""
ENV uvicorn_extras=$uvicorn_extras

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["poetry run prisma db push --schema prisma/schema.prisma && poetry run uvicorn app:app --host 0.0.0.0 --port 80 $uvicorn_extras"]
