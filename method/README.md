# Compositioner

This is a standalone module which can be installed and used without plants backend and frontend.

It contains methods to generate stable plants compotions.

## Preparetion

0. Prepare virtual environment with `venv` if you need
1. Install dependencies with `python -m pip install -r requirements.txt`

## Running an example

1. Set environment variables from [envfile](.env.example), you would need a database with plants, limitations and others
2. launch `make run-example` or launch manually with `python -m example`

## Installation

You can install this module to system by running `pip install .`.

Wheel can be built the same way, by running `python -m build .` (you would need to install `build` package before that).
To install package from .wheel, use `python -m wheel install dist/compositioner-0.1.0-py3-none-any.whl`

All commands are presented in Makefile for reference.