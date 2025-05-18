# Codex Playground

This repository contains a small FastAPI application with user authentication.

## Features
- Sign in page
- SQLite database for storing users by default
- Optional PostgreSQL support via the `DATABASE_URL` environment variable
- Protected page that greets authenticated users

## Development
Run the setup script to create a virtual environment and install dependencies:

```bash
./setup.sh
source venv/bin/activate
```

The script configures SQLite for local development. If you prefer PostgreSQL, install Docker manually and set the `DATABASE_URL` environment variable accordingly.

Run the application:

```bash
uvicorn app.main:app --reload
```

Run tests:

```bash
PYTHONPATH=. pytest
```

## Environment variables
- `DATABASE_URL` – SQLAlchemy connection string. Defaults to `sqlite:///./test.db` if unset.
- `TEST_DATABASE_URL` – Optional connection string used by the test suite. If unset, the tests use an in-memory SQLite database.
- `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_KEY` – Secrets used by the deploy GitHub Actions workflow. Obtain these from the target server administrator.

## Docker
A `Dockerfile` is provided for containerized deployment.

Build and run:

```bash
docker build -t codex-playground .
docker run -e DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres \
  -p 8000:80 codex-playground
```

The example above expects a PostgreSQL instance reachable at the hostname `db`. For local development you can run a Postgres container with:

```bash
docker run --name db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
```

Visit `http://localhost:8000/login` to sign in.
