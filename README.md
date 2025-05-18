# Codex Playground

This repository contains a small FastAPI application with user authentication.

## Features
- Sign in page
- SQLite database for storing users
- Protected page that greets authenticated users

## Development
Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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
docker run -p 8000:80 codex-playground
```

Visit `http://localhost:8000/login` to sign in.
