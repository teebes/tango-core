===================
 Introducing Tango
===================

The ``tango`` experiment: a preprocessor for the web.


WillowTree Apps: mobile application development shop


mashup
------

One viewport; many data sources.


desktop
-------

JavaScript in the browser.


mobile
------

1. Optimize for performance.

2. Target multiple client platforms natively.


server-side
-----------

Integrate with Python!

* urllib family
* requests
* screen-scape with lxml, pyquery
* json
* feedparser
* csv
* SQLAlchemy
* sqlite3
* ...


...in a web request?
--------------------

* slow blocking single thread
* async workers
* celery
* simple task queue (e.g. redis)


Wait a minute.
--------------

For read-only data with predictable arguments, it's the same work again and
again.  Let's process it once (or on a schedule) and serve up those results on
every following requests.

(Yes, we could cache, but we're talking about heavier processing here.)


Not just mashups.
-----------------

The tango project started to fix client data, normalize feeds, and stub out or
otherwise cover up non-existent data.  Also, to update content formats without
Apple review or user app upgrades.


Example
-------

(demo)


Another Web Framework?
----------------------

No. It's Flask.


Road of Open Source
-------------------

Just created public repository::

    http://github.com/willowtreeapps/tango-core

Have tests and many production applications for mining examples.

* Ron DuPlain <ron.duplain@gmail.com>
* WillowTree Apps, Inc. -- mobile application developers
* (We're hiring.)
