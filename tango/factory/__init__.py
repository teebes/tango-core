"Package to instantiate a Tango object from a Tango site package."

from flask import render_template, request
from werkzeug import create_environ

from tango.app import Tango
from tango.routes import get_routes
import tango.filters

from context import build_package_context
from snapshot import get_snapshot


def build_view(app, path, template, context):
    def view(*args, **kwargs):
        return render_template(template, **context)
    view.__name__ = path
    return app.route(path)(view)


def build_app(import_name, use_snapshot=True):
    """Create a Tango application object from a Python import name.

    Example, using the default site package in this project:
    >>> app = build_app('simplesite')
    >>> app.config['SITE']
    'simplesite'
    >>>
    """
    # Initialize application.
    app = Tango(import_name)
    app.config.from_object('tango.config')
    app.config.from_object(import_name + '.config')

    # Create app context, push it onto request stack for use in initialization.
    ctx = app.request_context(create_environ())
    ctx.push()

    # Load Tango filters.
    tango.filters.init_app(app)

    # Get routes.
    routes = get_routes(app)

    # Build template context, checking for a snapshot first.
    package_context = None
    if use_snapshot:
        package_context = get_snapshot(import_name)

    if package_context is None:
        package = __import__(import_name, fromlist=['content']).content
        package_context = build_package_context(package)
    else:
        print 'Using template context snapshot.'
    site_context = package_context.get(app.config['SITE'], {})
    app.site_context = site_context
    app.package_context = package_context

    # Stitch together context, template, and path.
    # TODO: Warn on mutually exclusive routes.py and context header routes.
    for template, paths in routes.items():
        for path in paths:
            build_view(app, path, template, site_context.get(path, {}))

    # Pop app request context.
    ctx.pop()

    app.context_processor(lambda: request.view_args)
    return app
