# Repo Instructions

## Testing
Run `source venv/bin/activate` to activate the python virtual environment
Run `PYTHONPATH=. pytest -q` to execute the test suite. Ensure it passes before committing changes.

## Editing setup.sh
The `setup.sh` file is used in creating codex-1 environments. I'm currently having issues getting it to read from the `requirements.txt` file. Please keep parity between installs in the `setup.sh` file and the `requirements.txt` file. Do not update the `setup.sh` file to directly read from the `requirements.txt` file.

# Setting up the Env
When working, assume there's a venv python environment with some pre-installed dependencies for you, as outlined in the setup.sh file.

# Writing Code
Don't forget to write tests.
