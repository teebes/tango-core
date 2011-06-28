=============================
 Tango: Mobile Web Framework
=============================

Tango is a web framework for mobile web development shops, built with Flask.


Overview
========

Tango targets users who are:

* template developers who implement mobile website designs.
* backend developers who source data for mobile websites.
* client developers who'd like to manage their own templates.

Initial focus is on template developers and backend developers.

Tango supports activities of:

* developing templates in a sandbox environment.
* sourcing site data from a mashup of sources,
  and building tools without any concern for web details.

Initial focus is on the relationship between templates and data sources.  Tango
completely separates site content from it's templates.  Template developers
work in a ``templates`` directory with pure Jinja2 templates and a ``static``
directory for assets, including but not limited to images, CSS, and JavaScript.
Backend developers work in a site ``stash`` package or module which
declaratively exports content into template contexts for given routes.

The templates, static assets, and stash modules are discovered and integrated
by the Tango core with the help of ``config.py`` and headers written in YAML.

See existing sites and examples for more detail.


What is Tango?
==============

Here is Tango's plan.


At a glance, Tango...
---------------------

* is a mobile web framework built on Python
* is a site-builder: follow a few simple conventions in a project and Tango
  builds a web application pushing scripted content into simple templates.
* provides device detection and capabilities, chooses template based on the
  user's device & browser
* includes general purpose automated testing for unit and functional tests


Benefits
--------

* Two teams develop Tango site packages in parallel:

 * template developers, implementing designs and arranging content
 * data sourcers, tapping into origin database or site to push content into
   templates

* Spec-first development

 * Tango site developers codify site's URL routes and data using Python & yaml
   definitions.
 * spec clearly spells out template content -- develop the spec as a collection
   of yaml headers, then develop templates & data at the same time

* Productivity Measures

 * Tango snapshots data - develop templates without fetching data
 * data sourcing occurs outside of web context - develop & unit-test data
   modules in isolation, in a simple scripting environment


Specifics
---------

* Tango deploys as a Python WSGI app:

 * complies with the WSGI web standard.
 * most deployments use mod_wsgi under Apache httpd.
 * can also deploy under ISAPI interface on Microsoft's IIS platform.

* Tango automates content and deployment on a schedule, including:

 * automated deploy using Python standards & automated upgrade using git
   revision control
 * cron static builds where possible
 * dynamic views with caching -- cached on a time-to-live schedule

* Tango site packages include

 * a template package in Python's Jinja2
 * a stash package in Python, using yaml headers, includes stashable content
 * static assets - images, CSS, JavaScript
 * config.py using simple key/value pairs

* Templating: Tango uses Python's highly regarded Jinja2 (inspired by Django).


Stashing Content
----------------

Stashable content is that which can be fetched up front and served to all
users.  In a Tango project, this content is scripted in Python modules, which
have structured metadata written in yaml.  When serving an application, the
Tango framework walks the ``sitename.stash`` package or module, building all of
the application view functions based on the yaml metadata.  Simple Tango sites
are just a ``stash`` package with a ``templates`` directory.  A simpler Tango
site is just a ``stash`` package with a config telling Tango to return json.
The simplest Tango site is single Python module, which is treated as a
``stash`` and is useful in building light APIs.


Dynamic Content
---------------

Pure dynamic content and forms require custom view functions.  In this case,
Tango builds an ``app`` object from the stash module, and this ``app`` object
allows for additional routes, view functions, and other features as provided by
Flask.  Projects without stashable content are effectively just Flask projects
which use utilities/tools provided by Tango.


Other Notes
-----------

Tango:

* framework reduces web request & response code to 0.
* developers can theme sites easily using template inheritance and CSS.
* is a rapid prototyping framework (think *very* rapid), but is ready for
  primetime & full applications.
* automates unit and functional tests, testing all the way up to (but not
  including) browser quirks.

On redirecting users from the desktop site:

* Most site owners target iPhone, Android, and Blackberry.

 * Nearly all of these devices have JavaScript enabled.
 * Use a simple JavaScript redirection script (preferably on every page, but at
   least the home page).

* For wider device targets:

 * Set URL rewrite rules for Apache httpd or IIS.
 * Redirect devices even if JavaScript is disabled.

On screen scraping:

* Sometimes the client data with the best structure is structured as (X)HTML.
* Tango does not have a general rule or silver bullet for screen scraping.
  Each case is treated specially.  Developers study the client's markup, decide
  which elements to select, and strip/cleanup attributes and tags as needed.
  Some origin elements and attributes flow through, others are mutated.  For
  maintenance, this requires a close eye on how the origin site changes.


Discussion Topics
=================

On Context
----------

Throughout the Tango project, there are two uses of the word "context":

* The Flask app current in context;
  here "context" is the same as used in the Flask project.
  (Flask has request contexts and context-locals.)
* The template context, a collection of variables available in the template;
  here "context" is the same as used in the Jinja project.


Logic in Templates?
-------------------

Template developers say that heavy logic should stay out of templates, and
there are good reasons for that.  In stark contrast, Tango relies on heavy
logic in the templates.  This is intentional; for stashable content, *all*
request-based logic is in the templates.  Where Tango stashes content, there
are no explicit view functions, only templates and a freestyle data layer.


Yet Another Web Framework?
--------------------------

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

The current release is 0.1 (Basico) which establishes Tango conventions
and package namespaces, supports building static sites, provides a pattern for
mixing stashable/cachable content and dynamic view functions, and provides a
solid codebase with 100% statement test coverage.

Further development beyond Tango Basico will support:

* utilities determining whether URL is internal or external to the mobile site.

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
