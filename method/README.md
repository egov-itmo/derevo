# Derevo library

This is a standalone module which can be installed and used without plants backend and frontend.

It contains methods to generate stable plants compotions.

## Installation

0. Prepare virtual environment with `venv` if you need
1. Install with `python -m pip install .`

Wheel can be built the same way, by running `python -m build .` (you would need to install `build` package before that).
To install package from .wheel, use `python -m wheel install dist/derevo-0.1.0-py3-none-any.whl`.

Following packages are need to be installed on your system to successfully build the module: `build virtualenv`

All commands are presented in Makefile for reference.

## Running an example

1. Set environment variables from [envfile](.env.example), you would need a database with plants, limitations and others
2. launch `make run-example` or launch manually with `python -m example`

## Packing in docker for a backend service

For the backend docker image to build, `derevo` must be installed in it. As they are in different directories,
  and `derevo` is not on PyPi yet, it was decided to be a best way to store built wheel rosource in a dummy
  container called `local/derevo`. It should be built using `make docker-build` before building backend image.


## Development

For development purposes it is better to use _editable install_ with `python -m pip install -e .` - so when you change
  the content of the module, there is no need to perform reinstall.

In some cases VS Code Pylance and other analyzer tools report missing module, then you need to either configure them
  properly (in case of Pylance, add `"python.analysis.extraPaths": ["<project_dir>/method"]`
  to .vscode/settings.json) or make a strict installation:
  `python -m pip install -e . --config-settings editable_mode=strict`.
  The second option is better, in case of adding new files a reinstallation will be needed
