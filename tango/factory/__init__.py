"Package to instantiate a Tango object from a Tango site package."

from flask import render_template

from tango.app import Tango
from tango.routes import get_routes

from context import build_package_context
from snapshot import get_snapshot


def build_view(app, path, template, context):
    def view(*args, **kwargs):
        return render_template(template, **context)
    view.__name__ = path
    return app.route(path)(view)


def build_app(import_name):
    """Create a Tango application object from a Python import name.

    Example, using the default site package in this project:
    >>> app = build_app('tango.site.default')
    >>> app.config['SITE']
    'default'
    >>>
    """
    # Initialize application.
    app = Tango(import_name)
    app.config.from_object('tango.config')
    app.config.from_object(import_name + '.config')

    # Get routes.
    routes = get_routes(app)

    # Build template context, checking for a snapshot first.
    package_context = get_snapshot(import_name)
    if package_context is None:
        package = __import__(import_name)
        package_context = build_package_context(package)
    else:
        print 'Using template context snapshot.'
    site_context = package_context.get(app.config['SITE'], {})
    app.site_context = site_context
    app.package_context = package_context

    # Stitch together context, template, and path.
    for template, paths in routes.items():
        for path in paths:
            build_view(app, path, template, site_context.get(path, {}))

    return app
