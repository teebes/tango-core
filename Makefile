# make: your onestop entry to this project, complete with dependency resolution

all: flakes test todo

setup = python setup.py
nosetests = python -W ignore::DeprecationWarning setup.py nosetests

clean:
	find . -name '*.py[co]' -delete
	rm -f develop README.html DEVELOPMENT.html tests/test_*.html
	rm -fr *.egg *.egg-info dist build
	rm -f *.dat

install:
	$(setup) install

develop: setup.py
	easy_install pip
	pip install Flask-Testing
	pip install nose nose-exclude minimock==1.2.5
	pip install coverage
	pip install pyflakes
	pip install docutils
	$(setup) develop
	touch develop

flakes: develop
	find . -name '*.py' | xargs pyflakes | grep -v local_config; true

test: develop
	$(nosetests) --with-coverage --cover-package=tango --cover-tests

smoke: develop
	$(nosetests) --stop

coverage: test

dist: develop
	# TODO: Build GitHub upload task `make publish`? GitHub support yet?
	$(setup) sdist
	@echo
	@echo Tarball for distribution:
	@echo `ls -1rt ./dist/*.tar* | tail -1`

distribute: dist

doc_files := $(patsubst %.rst,%.html,$(wildcard *.rst))
doc_deep_files := $(patsubst %.rst,%.html,$(wildcard **/*.rst))

doc: $(doc_files) $(doc_deep_files)

%.html: %.rst develop
	rst2html $< > $@


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
