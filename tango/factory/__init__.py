"Package to instantiate a Tango object from a Tango stash package."

from flask import jsonify, render_template, request
from werkzeug import create_environ

from tango.app import Tango
import tango
import tango.filters

from context import build_package_routes
from snapshot import get_snapshot


def build_view(app, route):
    template = route.template
    context = route.context

    # TODO: Create a tango.writers namespace.
    # TODO: Use writer as dictated by route, only define view once.
    # TODO: First look for template, then look for writer, then use default.
    # TODO: Use default as configured in app.config.
    if template is None:
        def view(*args, **kwargs):
            return jsonify(**context)
    else:
        def view(*args, **kwargs):
            return render_template(template, **context)
    view.__name__ = route.rule
    return app.route(route.rule)(view)


def build_app(import_name, use_snapshot=True):
    """Create a Tango application object from a Python import name.

    Example, using the simplesite package in this project:
    >>> app = build_app('simplesite')
    >>> app.config['SITE']
    'simplesite'
    >>>
    """
    # Initialize application.
    app = Tango(import_name)
    app.config.from_object('tango.config')
    app.config['TANGO_VERSION'] = tango.__fullversion__
    app.config['TANGO_MAINTAINER'] = tango.__contact__
    app.config.from_object(import_name + '.config')
    # Build label from config to allow override if so desired.
    app.config['TANGO_LABEL'] = \
        tango.build_label(app.config['TANGO_VERSION'],
                          app.config['TANGO_MAINTAINER'])

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
        package = __import__(import_name, fromlist=['stash']).stash
        routes = build_package_routes(package)
    else:
        print 'Using snapshot with stashed template context.'
    app.routes = routes

    # Stitch together context, template, and path.
    for route in app.routes:
        build_view(app, route)

    # Pop app request context.
    ctx.pop()

    app.context_processor(lambda: request.view_args)
    return app
