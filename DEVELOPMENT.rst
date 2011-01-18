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
>>> def call(command='tango'):
...     sys.argv = command.split(' ')
...     manage.run()
...
>>> mock('sys.exit', tracker=None)
>>> call()
  serve     Run a Tango site on the local machine, for development.
  shell     Open an interactive interpreter within a Tango site request context.
  version   Display this version of Tango.
  snapshot  Build context from a Tango site package and store it into an image file.
  build     Build a Tango site into a collection of static files.
>>> call('tango version') # doctest:+ELLIPSIS
Tango ...
Maintainer: ...
>>> call('tango snapshot default')
>>> call('tango build default')
>>> call('tango serve default')
>>> call('tango shell default')

Note that 'default' is the site name.
Use the sitename appropriate to your project.
e.g. sitename in tango.site.sitename
