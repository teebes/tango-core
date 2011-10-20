"Package to instantiate a Tango object from a Tango stash module."

from flask import request
from werkzeug import create_environ

import tango
import tango.filters
from tango.app import Tango
from tango.helpers import module_exists
from tango.templating import get_global_context, get_context_processors

from tango.factory.context import build_module_routes
from tango.factory.snapshot import get_snapshot


def build_app(import_name, use_snapshot=True):
    """Create a Tango application object from a Python import name.

    Example, using the simplesite module in this project:
    >>> app = build_app('simplesite')
    >>> app.url_map # doctest:+NORMALIZE_WHITESPACE
    Map([[<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
          <Rule '/' (HEAD, OPTIONS, GET) -> />]])
    >>>

    Example, using the a single module called simplest.py:
    >>> app = build_app('simplest')
    >>> app.url_map # doctest:+NORMALIZE_WHITESPACE
    Map([[<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
          <Rule '/' (HEAD, OPTIONS, GET) -> />]])
    >>>
    """
    # Initialize application.
    app = Tango(import_name)

    # Check for a site config.
    if module_exists(import_name + '.config'):
        app.config.from_object(import_name + '.config')

    # Create app context, push it onto request stack for use in initialization.
    ctx = app.request_context(create_environ())
    ctx.push()

    # Load Tango filters.
    tango.filters.init_app(app)

    # Build application routes, checking for a snapshot first.
    routes = None
    if use_snapshot:
        routes = get_snapshot(import_name)

    if routes is None:
        if module_exists(import_name + '.stash'):
            module = __import__(import_name, fromlist=['stash']).stash
        else:
            module = __import__(import_name)
        routes = build_module_routes(module)
    else:
        print 'Using snapshot with stashed template context.'
    app.routes = routes

    # Stitch together context, template, and path.
    for route in app.routes:
        app.build_view(route)

    # Add templating utilities contained in package.
    if module_exists(import_name + '.templating'):
        module = __import__(import_name, fromlist=['templating']).templating
        app.context_processor(lambda: get_global_context(module))
        for function in get_context_processors(module):
            app.context_processor(function)

    # Pop app request context.
    ctx.pop()

    app.context_processor(lambda: request.view_args)
    return app
