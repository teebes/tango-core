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

>>> from minimock import Mock, mock
>>> import code
>>> import tango.app
>>> mock('sys.exit', tracker=None)
>>> mock('code.interact')
>>> mock('tango.app.Tango.run')


Command line: ``tango``

>>> call()
... # doctest:+NORMALIZE_WHITESPACE
  snapshot  Build context from a Tango site package and store it into an image file.
  shell     Runs a Python shell inside Tango application context.
  serve     Run a Tango site on the local machine, for development.
  version   Display this version of Tango.
  build     Build a Tango site into a collection of static files.


Command line: ``tango version``

>>> call('version')
... # doctest:+ELLIPSIS
Tango ...
Maintainer: ...


Command line: ``tango build default``

>>> call('build default')


Command line: ``tango serve default``

>>> call('serve default')
Called tango.app.Tango.run(
    debug=True,
    host='127.0.0.1',
    port=5000,
    use_debugger=True,
    use_reloader=True)


Command line: ``tango snapshot default``

>>> call('snapshot default')
Snapshot of full template context: tango.site.default.dat


Command line: ``tango snapshot doesnotexist``

>>> call('snapshot doesnotexist')
No content package found for 'doesnotexist'.


Command line: ``tango serve default`` with snapshot available

>>> call('serve default')
Using template context snapshot.
Called tango.app.Tango.run(
    debug=True,
    host='127.0.0.1',
    port=5000,
    use_debugger=True,
    use_reloader=True)


Remove snapshot.
>>> import os
>>> os.system('rm -f tango.site.default.dat')
0


Command line: ``tango shell --no-ipython default``

>>> call('shell --no-ipython default')
... # doctest:+ELLIPSIS
Called code.interact('', local={'app': <tango.app.Tango object at 0x...>})


Command line: ``tango shell default`` with ipython option

>>> try:
...     import IPython
...     IPython.Shell.IPShellEmbed = Mock('IPython.Shell.IPShellEmbed')
...     IPython.Shell.IPShellEmbed.mock_returns = Mock('sh')
...     call('shell default')
... except ImportError:
...     print "Called IPython.Shell.IPShellEmbed(banner='')"
...     print ("Called sh(global_ns={}, local_ns={'app':"
...            " <tango.app.Tango object at 0x...>})")
... # doctest:+ELLIPSIS
Called IPython.Shell.IPShellEmbed(banner='')
Called sh(global_ns={}, local_ns={'app': <tango.app.Tango object at 0x...>})


Command line: ``tango shell default`` without ipython installed

>>> try:
...     import IPython
...     IPython = sys.modules.pop('IPython')
...     call('shell default')
...     sys.modules['IPython'] = IPython
... except:
...     call('shell default')
... # doctest:+ELLIPSIS
Called code.interact('', local={'app': <tango.app.Tango object at 0x...>})
