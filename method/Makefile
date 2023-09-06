SOURCE_DIR := derevo example tests
VERSION := 0.1.1

lint:
	pylint ${SOURCE_DIR}

format:
	black ${SOURCE_DIR}

test:
	pytest

test-short:
	pytest --tb=no

test-cov:
	pytest --cov

test-cov-html:
	$(info Saving coverage output is to coverage_html/index.html)
	pytest --cov --cov-report=html:coverage_html

run-example:
	USE_PYGEOS=0 python -m example

install:
	pip install .

install-dev:
	pip install -e '.[dev]' --config-settings editable_mode=strict

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
