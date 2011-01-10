# make: your onestop entry to this project, complete with dependency resolution

all: flakes test todo

clean:
	find . -name '*.py[co]' -delete
	rm -f develop
	rm -fr *.egg *.egg-info dist build

develop: setup.py
	easy_install pip
	pip install nose minimock
	pip install pyflakes
	python setup.py develop
	touch develop

flakes: develop
	find . -name '*.py' -exec pyflakes {} ';'

test: develop
	python -W ignore::DeprecationWarning setup.py nosetests

smoke: develop
	python -W ignore::DeprecationWarning setup.py nosetests --stop

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

.SILENT: flakes test todo
