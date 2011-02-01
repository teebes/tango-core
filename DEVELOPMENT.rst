========================================
 Developing Tango: Mobile Web Framework
========================================

Working on the Tango core framework?
With a working development environment::

    make test

This runs a series of automated tests.
You can add tests to docstrings or .rst documents.

See the various .rst docs and read through the source & git log.

For the Tango Basico release (``make todo | grep Basico``):

* TODO: Use 'routes' instead of 'path' in headers. (Basico)
* TODO: Use 'exports' instead of 'export' in headers. (Basico)
* TODO: Build a full production site with Tango Basico.


Todos:

* TODO: add simple unit test for tango.site.default '/' path.
* TODO: use tango.site.default in app context, update with target site.
* TODO: carefully catch ImportError - else hiding legitimate ImportErrors.
* TODO: support app.TAB tab completion with code.interact
* TODO: test empty and sparse site packages.
* TODO: Support regular expression route matches, using a 'match' directive.
  This matches routes.py, not request URLs, to support exports across an
  entire area of the app.
* TODO: Build a utility to determine if a link is internal/external to app.


Tool ideas:

* ``tango report <site>`` - where template devs, data devs, & managers meet

 * routes
 * static exports (hint is 'constant')
 * variable exports (displaying hints)
 * callable exports (hint is function signature + docstring)
 * templates (displaying routes)
 * template variables
 * missing templates

* general-use test tools, see below


Ideas for test tools for Tango sites:

* Walk routes, looking for 200 response on each route.
  Build a coverage report with this test, would this alone hit 100% statements?
* Report on exports which are not used
  and template variables which are not defined.
* Put these ideas together for a site tester which exercises 100% statements,
  looks for common errors.


Example header::

    site: sitename
    routes:
     - /page/<title>
     - match: /pages/.*
    exports:
     - title: Page # static export
     - content <- string # programmatic export with developer type hint
    routing:
     - title: get_page_titles # iterable or callable which returns an iterable
