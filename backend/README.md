# plants_api

This is an api to access plants data and update in by uploading a formed xlsx file.

## preparation

Currently `derevo` module is not on the PyPi, so it needs to be installed manually before running folowing
commands.

0. To install python dependencies (if you wish to run script without Docker)
  run `python -m pip install -r requirements.txt`. You may also want to use `venv` before that.
1. Prepare a PostgreSQL Server to store the database.
2. Go to ./plants_api/db and run `alembic upgrade head` to apply migrations. Do not forget to set environment variables
  `DB_ADDR`, `DB_PORT`, `DB_NAME`, `DB_USER` and `DB_PASS` (or list them in .env file) if they are different from
  default values.

## launching

Run backend locally with `make run` or `make debug`.

You can open [localhost:8080](http://localhost:8080) (or different host/port if you configured it)
  to get a redirect to Swagger UI with endpoints list.

## run in docker

0. Create .env file by copying and editing [env.example](env.example).
1. (optionally) change USER_WITH_SLASH variable in Makefile to your DockerHub username with tailing slash.
2. Build image with `make docker-build`.
3. Run a container with `make docker-run` (.env file variables will be used by Docker).

## configuration

You can change backend configuration by editing .env flie (got from `env.example`)
  or pass arguments as command-line parameters.

Run `python -m plants_api --help` to get help.
