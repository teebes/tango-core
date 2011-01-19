========================================
 Developing Tango: Mobile Web Framework
========================================

Working on the Tango core framework?
With a working development environment::

    make test

This runs a series of automated tests.
You can add tests to docstrings or .rst documents.


Testing: Command-line Interface
===============================

This section of the document tests Tango's command-line interface.
For each command below, note that 'default' is the site name.
Use the sitename appropriate to your project,
that is, sitename in tango.site.sitename

Import Tango's command-line module.

>>> from tango import manage


Build a test harness.

>>> import sys
>>> def call(command=None):
...     "Set command-line arguments and call Tango manager."
...     args = []
...     if command is not None:
...         args = command.split(' ')
...     previous_argv = sys.argv
...     sys.argv = ['tango/manage.py'] + args
...     manage.run()
...     sys.argv = previous_argv
...


Mock system-level details.

>>> from minimock import mock
>>> import tango.app
>>> mock('sys.exit', tracker=None)
>>> mock('tango.app.Tango.run')


Call: tango

>>> call()
... # doctest:+NORMALIZE_WHITESPACE
  snapshot  Build context from a Tango site package and store it into an image file.
  shell     Open an interactive interpreter within a Tango site request context.
  version   Display this version of Tango.
  serve     Run a Tango site on the local machine, for development.
  build     Build a Tango site into a collection of static files.


Call: tango version

>>> call('version')
... # doctest:+ELLIPSIS
Tango ...
Maintainer: ...


Call: tango snapshot default

>>> call('snapshot default')


Call: tango build default

>>> call('build default')


Call: tango serve default

>>> call('serve default')
Called tango.app.Tango.run(
    debug=True,
    host='127.0.0.1',
    port=5000,
    use_debugger=True,
    use_reloader=True)


Call: tango shell default

>>> call('shell default')


