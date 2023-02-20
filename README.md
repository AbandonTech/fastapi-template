# Abandon Tech FastAPI Template

This is a template project for FastAPI using PostgreSQL as well as Prisma for ORM + database migrations.

## First Time Install

Create your `.env` file in the root project directory, you can copy `.env.sample` as the base for this.

`docker compose up --build`

A sample User schema has been created to allow the prisma client to generate upon project creation. This should be
modified or deleted to fit your app's needs prior to creating any migrations.

## Migrations
This project is using [prisma](https://www.prisma.io/) as the ORM

### Pushing migrations to the database
The migrations can be pushed to the running postgresql container using the 
schema and migrations found in `./prisma/migrations`. 

```shell
prisma db push --schema prisma/schema.prisma
```

### Creating migrations
Migrations can be created by using this command, while the database is running.

```shell
prisma migrate dev --schema prisma/schema.prisma --name "what this change does"
```
