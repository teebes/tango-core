"Package to build a Tango site into a collection of static files."

import os

from flaskext.frozen import Freezer

from tango.errors import ConfigurationError


def build_static_site(app, path=None):
    """Build a Tango site into a collection of static files, based on routing.

    Uses Frozen-Flask to build the site.

    >>> from tango.factory import build_app
    >>> app = build_app('testsite')
    >>> del app.config['TANGO_BUILD_BASE']
    >>> build_static_site(app)
    Traceback (most recent call last):
        ...
    ConfigurationError: app config is missing TANGO_BUILD_BASE
    >>>
    """
    if path is None:
        sitepath = app.config['SITE'] or 'build'
        if not app.config.has_key('TANGO_BUILD_BASE'):
            raise ConfigurationError('app config is missing TANGO_BUILD_BASE')
        path = app.config['TANGO_BUILD_BASE'] + '/' + sitepath
    app.config['FREEZER_DESTINATION'] = path
    if not os.path.exists(path):
        os.makedirs(path)
    freezer = Freezer(app)

    @freezer.register_generator
    def routing():
        for rule in app.url_map.iter_rules():
            route_context = app.site_context.get(rule.endpoint)
            if route_context is None:
                continue
            routing = route_context.get('_routing')
            if routing is None:
                continue
            for argument, values in routing.items():
                for value in values:
                    if value is None:
                        continue
                    yield rule.endpoint, {argument: value}

    freezer.freeze()
    return app
