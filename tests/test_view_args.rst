Testing: Implicit View Function Arguments
=========================================

When defining routes, you can define URL parameters in your rules, just as in
Werkzeug and Flask.  For convenience, Tango provides these parameters by name
in the template context.  So if you define::

    /my/<argument>

and you get a request for::

    /my/value

your templates will have in their context ``argument`` with value ``'value'``.

Let's test it.  Start by building a Tango application.

>>> from tango.factory.app import build_app
>>> app = build_app('testsite', import_stash=True)

Create a test client.

>>> client = app.test_client()

Our route is ``/argument/<argument>/`` and the routed template only contains::

    argument: {{ argument }}

>>> client.get('/argument/testing/').data
'argument: testing'
>>>

>>> client.get('/argument/this_is_my_argument/').data
'argument: this_is_my_argument'
>>>

I'm convinced this works.  Are you convinced?
