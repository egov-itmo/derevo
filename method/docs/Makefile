clean:
	rm -rf ./build

autodoc:
	sphinx-apidoc -f -o source/components ../derevo/
	rm source/components/modules.rst

build: autodoc
	sphinx-build -M html source build
