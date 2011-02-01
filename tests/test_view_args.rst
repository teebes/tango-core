Testing: Implicit View Function Arguments
=========================================

When defining routes, you can define URL parameters in your rules, just as in
Werkzeug and Flask.  Tango provides these parameters by name in the template
context.  So if you define::

    /my/<argument>

and you get a request for::

    /my/value

your templates will have in their context ``argument`` with value ``'value'``.

Let's test it.  Start by building a Tango application.

>>> from tango.factory import build_app
>>> app = build_app('tango.site.test')

Create a test client.

>>> client = app.test_client()

Our route is ``/routing/<parameter>`` and the routed template only contains::

    {{ parameter }}

>>> client.get('/routing/testing').data
'testing'

>>> client.get('/routing/this_is_my_parameter').data
'this_is_my_parameter'

I'm convinced.  Are you convinced?
