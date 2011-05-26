Testing: Command-line Interface
===============================

For each command below, note that 'simplesite' is the site name.
In production, use the sitename appropriate to your project.

Import Tango's command-line module.

>>> from tango import manage


Build a test harness.

>>> import os
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
>>>


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
  snapshot  Pull context from a stashable Tango site and store it into an image file.
  shell     Runs a Python shell inside Tango application context.
  serve     Run a Tango site on the local machine, for development.
  version   Display this version of Tango.
  build     Build a Tango site into a collection of static files.
>>>


Command line: ``tango version``

>>> call('version')
... # doctest:+ELLIPSIS
Tango ...
Maintainer: ...
>>>


Command line: ``tango build default``

>>> call('build simplesite')
Successfully built site: simplesite
>>>


Remove build.
>>> os.system('rm -fr simplesite/')
0
>>>


Command line: ``tango serve default``

>>> call('serve simplesite')
Called tango.app.Tango.run(
    debug=True,
    host='127.0.0.1',
    port=5000,
    use_debugger=True,
    use_reloader=True)
>>>


Command line: ``tango snapshot default``

>>> call('snapshot simplesite')
Snapshot of full stashable template context: simplesite.dat
>>>


Command line: ``tango serve default`` with snapshot available

>>> call('serve simplesite')
Using snapshot with stashed template context.
Called tango.app.Tango.run(
    debug=True,
    host='127.0.0.1',
    port=5000,
    use_debugger=True,
    use_reloader=True)
>>>


Remove snapshot.
>>> import os
>>> os.system('rm -f simplesite.dat')
0
>>>


Command line: ``tango shell --no-ipython default``

>>> call('shell --no-ipython simplesite')
... # doctest:+ELLIPSIS
Called code.interact('', local={'app': <tango.app.Tango object at 0x...>})
>>>


Command line: ``tango shell default`` with ipython option

>>> try:
...     import IPython
...     IPython.Shell.IPShellEmbed = Mock('IPython.Shell.IPShellEmbed')
...     IPython.Shell.IPShellEmbed.mock_returns = Mock('sh')
...     call('shell simplesite')
... except ImportError:
...     print "Called IPython.Shell.IPShellEmbed(banner='')"
...     print ("Called sh(global_ns={}, local_ns={'app':"
...            " <tango.app.Tango object at 0x...>})")
... # doctest:+ELLIPSIS,+NORMALIZE_WHITESPACE
Called IPython.Shell.IPShellEmbed(banner='')
Called sh(...global_ns={}, local_ns={'app': <tango.app.Tango object at 0x...>})
>>>


Command line: ``tango shell default`` without ipython installed

>>> try:
...     import IPython
...     IPython = sys.modules.pop('IPython')
...     call('shell simplesite')
...     sys.modules['IPython'] = IPython
... except:
...     call('shell simplesite')
... # doctest:+ELLIPSIS
Called code.interact('', local={'app': <tango.app.Tango object at 0x...>})
>>>


Test for cases where site does not exist.
>>> from minimock import restore
>>> restore()

Command line: ``tango build doesnotexist``

>>> call('build doesnotexist')
Traceback (most recent call last):
    ...
SystemExit: 7
>>>


Command line: ``tango serve doesnotexist``

>>> call('serve doesnotexist')
Traceback (most recent call last):
    ...
SystemExit: 7
>>>


Command line: ``tango snapshot doesnotexist``

>>> call('snapshot doesnotexist')
Traceback (most recent call last):
 ...
SystemExit: 7
>>>


Command line: ``tango shell doesnotexist``

>>> call('shell doesnotexist')
Traceback (most recent call last):
    ...
SystemExit: 7
>>>


Verify call from OS shell.

>>> os.system('tango version >/dev/null 2>&1')
0
>>>
