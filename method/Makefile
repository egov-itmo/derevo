SOURCE_DIR := compositioner example

lint:
	python -m pylint ${SOURCE_DIR}

format:
	python -m black ${SOURCE_DIR}

run-example:
	USE_PYGEOS=0 python -m example

install:
	python -m pip install .

clean:
	rm -rf ./build ./dist ./pg_save.egg-info

udpate-pypi: clean
	python -m build . --no-isolation
	python -m twine upload  dist/*

install-from-build:
	python -m wheel install dist/pg_save-*.whl