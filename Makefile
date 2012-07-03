# make: your onestop entry to this project, complete with dependency resolution

all: flakes test todo

setup = python setup.py
nosetests = python -W ignore::DeprecationWarning setup.py nosetests
tarball = `ls -1rt ./dist/*.tar* | tail -1`
pypi_update = $(setup) sdist upload

clean:
	find . -name '*.py[co]' -delete
	rm -f develop README.html DEVELOPMENT.html tests/test_*.html
	rm -f README.aux README.dvi README.log README.out README.pdf README.tex
	rm -fr *.egg *.egg-info dist build
	rm -f *.dat

install:
	$(setup) install

develop: setup.py
	easy_install pip
	easy_install tox
	easy_install Flask-Testing
	easy_install nose nose-exclude minimock==1.2.5
	easy_install coverage
	easy_install pyflakes
	easy_install docutils
	$(setup) develop
	touch develop

flakes: develop
	find . -name '*.py' | grep -v .tox | xargs pyflakes | grep -v local_config; true

test: develop
	$(nosetests) --with-coverage --cover-package=tango --cover-erase

full-test: develop
	tox

test_flask: develop
	python tests/test_flask.py

smoke: develop
	$(nosetests) --stop

coverage: test

dist: develop
	$(setup) sdist
	@echo
	@echo Tarball for distribution:
	@echo $(tarball)

distribute: dist

publish:
	$(pypi_update)

doc_files := $(patsubst %.rst,%.html,$(wildcard *.rst))
doc_deep_files := $(patsubst %.rst,%.html,$(wildcard **/*.rst))

doc: $(doc_files) $(doc_deep_files) README.pdf

%.html: %.rst develop
	rst2html $< > $@

README.pdf: README.dvi
	dvipdf $<

README.dvi: README.tex
	latex $<

README.tex: README.rst
	rst2newlatex $< > $@

# Here is a custom todo tool, documented clearly so you know it works.
# If we write capital tee oh dee oh literally, `make todo` will list Makefile.
# We don't want that.  We want to find actual todos in the project.
# The sed expression below normalizes whitespace within one tab-stop.
# In the sed expression, we match [^T\ODO]* to avoid .* chopping off lines.
# Dummy regular expression brackets [T] don't do anything to our grep call.
# Dummy escape \O is literal O, which is used to avoid matching Makefile.
todo:
	echo
	echo "T"ODOs:
	echo
	grep -nR [T]ODO * | sed 's/\([0-9]\):[^T\ODO]*T\ODO/\1:\tT\ODO/g'
	echo

.PHONY: dist
.SILENT: coverage dist flakes test todo
