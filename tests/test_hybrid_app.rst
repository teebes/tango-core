Testing: Extending App Objects Built By Stash, i.e. Hybrid Apps
===============================================================

You can build an app object from a project's stash, then extend the application
using the vanilla Flask APIs.

Let's try it.  Start by building a Tango application.

>>> from tango.factory.app import build_app
>>> app = build_app('simplesite')

Create a test client.

>>> client = app.test_client()

We're going to add a view function at ``/hybrid/``.
Note it doesn't exist in the stash.

>>> client.get('/hybrid/').status_code
404
>>>


However, the stash does have other view functions.

>>> client.get('/').status_code
200
>>>


Now add the view function.

>>> @app.route('/hybrid/')
... def hybrid():
...     return 'This view function was added after stash.'
>>>


Finally, access the view function.

>>> response = client.get('/hybrid/')
>>> response.status_code
200
>>> print response.data
This view function was added after stash.
>>>
