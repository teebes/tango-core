"Package to instantiate a Tango object from a Tango stash module."

from flask import request
from werkzeug import create_environ

from tango.app import Tango
from tango.imports import module_exists
import tango
import tango.filters

from tango.factory.context import build_module_routes
from tango.factory.snapshot import get_snapshot


def get_app(site, **options):
    """Get a Tango app object from a site by the given import name.

    This function looks for an object named app in the package or module
    matching the import name provided by the given argument, and if it does not
    exist, builds an app from the stash inside the package or module.

    Hybrid apps, those with both stash and dynamic views, start with an app
    built from stash, then extend the app through the Flask API.

    >>> get_app('simplesite') # doctest:+ELLIPSIS
    <tango.app.Tango object at 0x...>
    >>> get_app('testsite') # doctest:+ELLIPSIS
    <tango.app.Tango object at 0x...>
    >>> get_app('importerror') # doctest:+ELLIPSIS
    Traceback (most recent call last):
      ...
    ImportError: No module named doesnotexist
    >>>
    """
    module = __import__(site)
    # Prefer app defined in module over a newly built app from the site stash.
    app = getattr(module, 'app', None)
    if app is not None:
        return app
    return build_app(site, **options)


def build_app(import_name, import_stash=False, use_snapshot=True,
              report_file=None):
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
        build_options = {'import_stash': import_stash}
        build_options['report_file'] = report_file
        routes = build_module_routes(module, **build_options)
    else:
        print 'Using snapshot with stashed template context.'
    app.routes = routes

    # Stitch together context, template, and path.
    for route in app.routes:
        app.build_view(route)

    # Pop app request context.
    ctx.pop()

    app.context_processor(lambda: request.view_args)
    return app
