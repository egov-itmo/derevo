SOURCE_DIR := derevo example
VERSION := 0.1.1

lint:
	pylint ${SOURCE_DIR}

format:
	black ${SOURCE_DIR}

run-example:
	USE_PYGEOS=0 python -m example

install:
	pip install .

install-dev:
	pip install -e . --config-settings editable_mode=strict

build:
	python -m build .

clean:
	rm -rf ./build ./dist ./derevo.egg-info

udpate-pypi: clean build
	python -m twine upload  dist/*

install-from-build:
	python -m wheel install dist/derevo-*.whl

docker-build:
	docker build --tag local/derevo:$(VERSION) .
	docker tag local/derevo:$(VERSION) local/derevo:latest
