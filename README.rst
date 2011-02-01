=============================
 Tango: Mobile Web Framework
=============================

Tango is a web framework for mobile web development shops, built on Flask.

Overview
========

Tango targets users who are:

* template developers who implement mobile website designs.
* backend developers who source data for mobile websites.
* client developers who'd like to manage their own templates.

Initial focus is on template developers and backend developers.

Tango supports activities of:

* developing templates in a sandbox environment.
* sourcing site data outside of web contexts.

Initial focus is on the relationship between templates and data sources.  Tango
completely separates site content from it's templates.  Template developers
work in a ``templates`` directory with pure Jinja2 templates and a ``static``
directory for assets, including but not limited to images, CSS, and JavaScript.
Backend developers work in a site ``content`` package which declaratively
exports template contexts for given routes.

The templates, static assets, and content package are discovered and integrated
by the Tango core with the help of ``config.py`` and ``routes.py`` in the site
package.  Site packages have the namespace::

    tango.site.sitename

See existing sites and examples for more detail.


What is Tango?
==============

Here is Tango's plan.


At a glance, Tango...
---------------------

* is a mobile web framework built on Python
* is a site-builder: follow a few simple conventions in your project and Tango
  builds a mobile-optimized web app for you
* provides device detection and capabilities, chooses template based on the
  user's device & browser
* includes automated testing for unit and functional tests


Benefits
--------

* Two teams develop Tango site packages in parallel:

 * template developers, implementing designs and arranging content
 * data sourcers, tapping into origin database or site to push content into
   templates

* Spec-first development

 * Tango site developers codify site's URL routes and data using Python & yaml
   definitions.
 * spec clearly spells out template content -- template & data are developed at
   the same time

* Productivity Measures

 * Tango snapshots data - develop templates without fetching data
 * data sourcing occurs outside of web context - develop & unit-test data
   modules in isolation


Specifics
---------

* Tango deploys as a Python WSGI app.

 * Tango complies with the WSGI web standard.
 * Most Tango deployments use mod_wsgi under Apache httpd.
 * Tango can also deploy under ISAPI interface on Microsoft's IIS platform.

* Tango on a schedule, including:

 * automated deploy using Python standards & automated upgrade using git
   revision control
 * cron static builds where possible
 * dynamic views with caching -- cached on a time-to-live schedule

* Tango site packages include

 * a URL map using intuitive Python syntax (routes.py)
 * a template package in Python's Jinja2
 * a content package in Python, using yaml headers
 * static assets - images, CSS, JavaScript
 * config using simple key/value pairs

* Templating: Tango uses Python's highly regarded Jinja2 (inspired by Django).


Other Notes
-----------

Tango:

* framework reduces web request & response code to 0.
* developers can theme sites easily using template inheritance and CSS.
* is a rapid prototyping framework (we think *very* rapid), but is ready for
  primetime & full applications.
* automates unit and functional tests, testing all the way up to (but not
  including) browser quirks.

On redirecting users from the desktop site:

* Most site owners want to hit iPhone, Android, and Blackberry.

 * Nearly all of these devices have JavaScript enabled.
 * Use a simple JavaScript redirection script (preferably on every page, but at
   least the home page).

* For wider device targets:

 * Set URL rewrite rules for Apache httpd or IIS.
 * Redirect devices even if JavaScript is disabled.


Logic in Templates?
===================

Template developers say you should keep heavy logic out-of-templates, and there
are good reasons for that.  In stark contrast, Tango relies on heavy logic in
the templates.  This is intentional; *all* logic is in the templates.  There
are no view functions in Tango, only templates and a data layer.


Yet Another Web Framework?
==========================

No, Tango extends Flask, or rather, Tango *builds* Flask, Flask WSGI
application objects to be exact.  Flask:

* builds on Werkzeug, a WSGI implementation
* builds on Jinja2, a templating platform
* allows for a Pythonic app-building pattern
* provides for extensions with clear conventions
  (and the Flask committers review & approve these extensions)

Tango focuses on the templating platform, completely hides the WSGI layer,
establishes a spec-first development pattern on top of Flask, leverages
Flask-related tools & extensions, and as a result, makes the Tango developers
more productive in building mobile web sites.

Tango is WillowTree's Flask platform, but is developed for general use.


Releases
========

The current target release is 0.1 (Basico) which establishes Tango conventions
and package namespaces, supports building static sites, and provides a solid
codebase with 100% statement test coverage.

Further development beyond Tango Basico will support:

* utilities determining whether URL is internal or external to the mobile site.
* simplified dynamic view functions.

Future development:

* Establish and implement simple conventions for partial templates targeting
  specific devices.
* Provide a configurable pipeline for common optimizations of responses.
* Provide a configurable pipeline for integrating addons into responses.
* Dynamic view caching, on an expiration schedule.
* Static context updates on a schedule, for example, fetch a feed every 5 min.
* Consider developing an interface for clients to manage templates and content.


License
=======

Commercial.

Copyright 2010-2011, WillowTree Apps, Inc.  All rights reserved.  DO NOT COPY.
http://wtcg.basecamphq.com/projects/5158831/log
