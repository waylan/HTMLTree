# HTMLTree makefile

.PHONY : help
help:
	@echo 'Usage: make <subcommand>'
	@echo ''
	@echo 'Subcommands:'
	@echo '    install       Install HTMLTree locally'
	@echo '    release       Register and upload a new release to PyPI'
	@echo '    build         Build a source distribution'
	@echo '    test          Run all tests'
	@echo '    clean         Clean up the source directories'

.PHONY : install
install:
	python setup.py install

.PHONY : release
deploy:
	python setup.py register
	python setup.py sdist --formats zip,gztar bdist_wheel upload

.PHONY : build
build:
	python setup.py sdist --formats zip,gztar bdist_wheel

.PHONY : test
test:
	tox

.PHONY : clean
clean:
	rm -f MANIFEST
	rm -f *.pyc
	rm -rf build
	rm -rf dist
