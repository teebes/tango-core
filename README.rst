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

See the examples for more detail.


Releases
========

The current target release is 0.1 (Basico) which establishes Tango conventions,
namespaces, and supports building static sites.

Further development beyond Tango Basico will support:

* arguments in site routes.
* view functions in addition to exporting static template contexts.

Future development:

* Establish and implement simple conventions for partial templates targeting
  specific devices.
* Provide a configurable pipeline for common optimizations of responses.
* Provide a configurable pipeline for integrating addons into responses.
* Consider developing an interface for clients to manage templates and content.


License
=======

Commercial.

Copyright 2010-2011, WillowTree Apps, Inc.  All rights reserved.  DO NOT COPY.
http://wtcg.basecamphq.com/projects/5158831/log
