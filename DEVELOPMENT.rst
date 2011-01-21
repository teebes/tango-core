========================================
 Developing Tango: Mobile Web Framework
========================================

Working on the Tango core framework?
With a working development environment::

    make test

This runs a series of automated tests.
You can add tests to docstrings or .rst documents.

See the various .rst docs and read through the source & git log.


Todos:

* TODO: add simple unit test for tango.site.default '/' path.
* TODO: split tango.site.default and tango.site.test.
* TODO: use tango.site.test in tests.
* TODO: use tango.site.default in app context, update with target site.
* TODO: carefully catch ImportError - else hiding legitimate ImportErrors.
* TODO: support app.TAB tab completion with code.interact
* TODO: test empty and sparse site packages.
