Testing: Command-line Interface
===============================

For each command below, note that 'simplesite' is the site name.
In production, use the sitename appropriate to your project.

Import Tango's command-line module.

>>> import tango.manage


Build a test harness.

>>> import os
>>> import sys
>>> def call(command=None):
...     "Set command-line arguments and call Tango manager."
...     args = []
...     if command is not None:
...         args = command.split(' ')
...     previous_argv = sys.argv
...     sys.argv = ['tango'] + args
...     tango.manage.run()
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
 Please provide a command
  snapshot  Pull context from a stashable Tango site and store it into an image file.
  shell     Runs a Python shell inside Tango application context.
  serve     Run a Tango site on the local machine, for development.
  version   Display this version of Tango.
  shelve    Shelve an application's stash, as a worker process.
>>>


Command line: ``tango version``

>>> call('version')
... # doctest:+ELLIPSIS
Tango ...
Maintainer: ...
>>>


Command line: ``tango serve simplesite``

>>> call('serve simplesite')
Called tango.app.Tango.run(
    debug=True,
    host='127.0.0.1',
    port=5000,
    use_debugger=True,
    use_reloader=True)
>>>


Command line: ``tango snapshot simplesite``

>>> call('snapshot simplesite')
Snapshot of full stashable template context: simplesite.dat
>>>


Command line: ``tango serve simplesite`` with snapshot available

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


Command line: ``tango shelve testsite`` (twice)

>>> call('shelve testsite')
Loading testsite.stash ... done.
Loading testsite.stash.blankexport ... done.
Loading testsite.stash.blankrouting ... done.
Loading testsite.stash.emptyrouting ... done.
Loading testsite.stash.index ... done.
Loading testsite.stash.multiple ... done.
Loading testsite.stash.noexports ... done.
Loading testsite.stash.norouting ... done.
Loading testsite.stash.package.module ... done.
Loading testsite.stash.routing ... done.
Stashing test / ... done.
Stashing test /another/<argument>/ ... done.
Stashing test /blank/export.txt ... done.
Stashing test /blank/routing.txt ... done.
Stashing test /files/page-<parameter>.html ... done.
Stashing test /index.json ... done.
Stashing test /norouting/<parameter>/ ... done.
Stashing test /plain/<routing>.txt ... done.
Stashing test /plain/exports.txt ... done.
Stashing test /route1.txt ... done.
Stashing test /route2.txt ... done.
Stashing test /routing/<parameter>/ ... done.
>>>

>>> call('shelve testsite')
Loading testsite.stash ... done.
Loading testsite.stash.blankexport ... done.
Loading testsite.stash.blankrouting ... done.
Loading testsite.stash.emptyrouting ... done.
Loading testsite.stash.index ... done.
Loading testsite.stash.multiple ... done.
Loading testsite.stash.noexports ... done.
Loading testsite.stash.norouting ... done.
Loading testsite.stash.package.module ... done.
Loading testsite.stash.routing ... done.
Stashing test / ... done.
Stashing test /another/<argument>/ ... done.
Stashing test /blank/export.txt ... done.
Stashing test /blank/routing.txt ... done.
Stashing test /files/page-<parameter>.html ... done.
Stashing test /index.json ... done.
Stashing test /norouting/<parameter>/ ... done.
Stashing test /plain/<routing>.txt ... done.
Stashing test /plain/exports.txt ... done.
Stashing test /route1.txt ... done.
Stashing test /route2.txt ... done.
Stashing test /routing/<parameter>/ ... done.
>>>


Command line: ``tango shell --no-ipython simplesite``

>>> call('shell --no-ipython simplesite')
... # doctest:+ELLIPSIS
Called code.interact('', local={'app': <tango.app.Tango object at 0x...>})
>>>


Command line: ``tango shell simplesite`` with ipython option

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


Command line: ``tango shell simplesite`` without ipython installed

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


Command line: ``tango serve doesnotexist``

>>> call('serve doesnotexist')
Traceback (most recent call last):
    ...
SystemExit: 66
>>>


Command line: ``tango snapshot doesnotexist``

>>> call('snapshot doesnotexist')
Traceback (most recent call last):
 ...
SystemExit: 66
>>>


Command line: ``tango shell doesnotexist``

>>> call('shell doesnotexist')
Traceback (most recent call last):
    ...
SystemExit: 66
>>>


Command line: ``tango shelve doesnotexist``

>>> call('shelve doesnotexist')
Traceback (most recent call last):
    ...
SystemExit: 66
>>>


Flask-Script v0.3.1 was swallowing IndexError exceptions.  Verify that the
current packaging scheme for this project flows an IndexError through.

Command line: ``tango shell indexerror``

>>> call('shell indexerror')
Traceback (most recent call last):
    ...
IndexError: Flask-Script v0.3.1 was swallowing IndexError exceptions.
>>>


Verify call from OS shell.

>>> os.system('tango version >/dev/null 2>&1')
0
>>>
