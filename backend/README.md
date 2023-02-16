# plants_api

This is an api to get plants data.

## preparation

0. To install python dependencies (if you wish to run script without Docker) run `python -m pip install -r requirements.txt`.  
1. Go to [database directory](../database/README.md) and follow the instructions on how to prepare a database.
2. Go to ./plants_api/db and run `alembic upgrade head` to apply migrations. Do not forget to set environment variables
  `DB_ADDR`, `DB_PORT`, `DB_NAME`, `DB_USER` and `DB_PASS` if they are different from default values.

## launching

Run backend locally with `make run`

## run in docker

0. Create .env file by copying and editing [env.example](env.example)
1. (optionally) change USER_WITH_SLASH variable in Makefile to your DockerHub username with tailing slash.
2. Build image with `make docker-build`
3. Run a container with `make docker-run` (.env file variables will be used by Docker)

## configuration

You can change backend configuration by editing .env flie (got from `env.example`) or pass arguments as command-line parameters.  
Run `python -m plants_api --help` to get help.
