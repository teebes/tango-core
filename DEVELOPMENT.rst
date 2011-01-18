========================================
 Developing Tango: Mobile Web Framework
========================================

Working on the Tango core framework?
With a working development environment::

    make test

This runs a series of automated tests.
You can add tests to docstrings or .rst documents.

>>> import sys
>>> from minimock import mock
>>> from tango import manage
>>>
>>> previous_argv = sys.argv
>>> def call(command=None):
...     "Set command-line arguments and call Tango manager."
...     args = []
...     if command is not None:
...         args = command.split(' ')
...     sys.argv = ['tango/manage.py'] + args
...     manage.run()
...
>>> mock('sys.exit', tracker=None)
>>> call() # doctest:+NORMALIZE_WHITESPACE
  snapshot  Build context from a Tango site package and store it into an image file.
  shell     Open an interactive interpreter within a Tango site request context.
  version   Display this version of Tango.
  serve     Run a Tango site on the local machine, for development.
  build     Build a Tango site into a collection of static files.
>>> call('version') # doctest:+ELLIPSIS
Tango ...
Maintainer: ...
>>> call('snapshot default')
>>> call('build default')
>>> call('serve default')
>>> call('shell default')
>>> sys.argv = previous_argv

Note that 'default' is the site name.
Use the sitename appropriate to your project.
e.g. sitename in tango.site.sitename
