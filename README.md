# Codex Playground

This repository contains a small FastAPI application with user authentication.

## Features
- Sign in page
- SQLite database for storing users by default
- Optional PostgreSQL support via the `DATABASE_URL` environment variable
- Protected page that greets authenticated users

## Development
Run the setup script to create a virtual environment and install dependencies.
The script also cleans up any `apt.llvm.org` entries from the system's APT
sources before installing Docker:

```bash
./setup.sh
source venv/bin/activate
```

The setup script attempts to install and start a local PostgreSQL server if
`apt-get` is available. The application will use SQLite unless the
`DATABASE_URL` environment variable is set. For development, you can run

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest
```

## Docker
A `Dockerfile` is provided for containerized deployment.

Build and run:

```bash
docker build -t codex-playground .
docker run -e DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres \
  -p 8000:80 codex-playground
```

The example above expects a PostgreSQL instance reachable at the hostname `db`.
For local development you can run a Postgres container with:

```bash
docker run --name db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
```

Visit `http://localhost:8000/login` to sign in.
