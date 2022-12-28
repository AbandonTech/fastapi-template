# Abandon Tech FastAPI Template

This is a template project for FastAPI using PostgreSQL as well as Prisma for ORM + database migrations.

## First Time Install

Create your `.env` file in the root project directory, you can copy `.env.sample` as the base for this.

`docker compose up --build`

The first build will result in an error that the Prisma client has not been generated yet. In order to fix this,
exec into your docker container and in the directory containing the `/prisma` directory (the root directory), run the
command `prisma generate`. You will need to restart the container, and you should be able to access the test route at
`localhost:8000/`.

A sample User schema has been created to allow the prisma client to generate upon project creation. This should be
modified or deleted to fit your app's needs prior to creating any migrations.

## Migrations
This project is using [prisma](https://www.prisma.io/) as the ORM

### Pushing migrations to the database
The migrations can be pushed to the running postgresql container using the 
schema and migrations found in `./backend/database`. 

```shell
prisma db push --schema backend/prisma/prisma.schema
```

### Creating migrations
Migrations can be created by using this command, while the database is running.

```shell
prisma migrate dev --schema backend/prisma/schema.prisma --name "what this change does"
```
