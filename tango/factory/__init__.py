"Package to instantiate a Tango object from a Tango site package."

from tango.app import Tango
from tango.routes import get_routes


def create_app(import_name):
    """Create a Tango application object from a Python import name.

    Example, using the default site package in this project:
    >>> app = create_app('tango.site.default')
    >>> app.config['SITE']
    'default'
    >>>
    """
    app = Tango(import_name)
    app.config.from_object(import_name + '.config')
    for template, urls in get_routes(app).items():
        "Stitch together context, template, and url."
        pass
    return app
