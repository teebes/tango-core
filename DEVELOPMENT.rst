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

* TODO: support app.TAB tab completion with code.interact
* TODO: Build a utility to determine if a link is internal/external to app.


Tool ideas:

* ``tango report <site>`` - where template devs, data devs, & managers meet

 * routes
 * static exports
 * variable exports
 * callable exports
 * provide hints by inspecting exports
 * templates (displaying routes)
 * template variables
 * missing templates

* general-use test tools, see below


Ideas for test tools for Tango sites:

* Walk routes, looking for 200 response on each route.
* Build a coverage report when stash is imported.
* Report on exports which are not used
  and template variables which are not defined.
* Put these ideas together for a site tester which exercises 100% statements,
  looks for common errors.


See test projects in ``tests/`` directory for example headers.
