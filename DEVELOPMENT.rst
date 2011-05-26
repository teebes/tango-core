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


Todos:

* TODO: add simple unit test for simplesite '/' path.
* TODO: support app.TAB tab completion with code.interact
* TODO: test empty and sparse site packages.
* TODO: Support pattern matching in routes.
* TODO: Build a utility to determine if a link is internal/external to app.
* TODO: Provide an app-building option which only hits a specific context
  module, for testing data/template integration in isolation.
  Remove any routes/templates mismatch warnings when using this option.


Open development topics:

* Build a tango toolkit, where a single .py file can be installed into a app
  that loads all stash modules installed to it.  This provides an "instant api"
  for native and web developers.  These modules are namespaced by the site
  directive in the module yaml metadata.  As an enhancement, allow for multiple
  sites to be listed for shared stash modules.
* For each of the following topics, look to available WSGI tools for solutions.
* For ``tango snapshot``, pickling only works for simple static
  content. Python's pickle protocol does not support generators or functions.
  How should snapshots work, or are they needed at all?
* How should tango handle app initialization?  One approach is to mix
  statically built content with app objects.  Another is to defer prefetched
  content so that a WSGI server can load an app instantly even before it's
  package context is available.  The latter gets complicated, whereas the
  former can be slow (unless snapshots come through here).  In either case,
  there is a sense of hot-swapping content of production applications.
  This is where much of tango's optimization takes place.
* Support multiple site builds in one project.  Allow for a list of site names
  to be provided in a module's metadata (currently the site directive uses only
  one site name).  On ``tango build``, output to <build_dir>/site1 and
  <build_dir>/site2.


Tool ideas:

* ``tango report <site>`` - where template devs, data devs, & managers meet

 * routes
 * static exports
 * variable exports
 * callable exports
 * provide hints based on type of export
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
     - content # programmatic export
    routing:
     - title: get_page_titles # iterable
