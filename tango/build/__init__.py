"Package to build a Tango site into a collection of static files."

import os

from flaskext.frozen import Freezer

from tango.errors import ConfigurationError


def build_static_site(app, output=None):
    """Build a Tango site into a collection of static files, based on routing.

    Uses Frozen-Flask to build the site.

    >>> from tango.factory import build_app
    >>> app = build_app('testsite')
    >>> del app.config['TANGO_BUILD_DIR']
    >>> app = build_app('testsite')
    >>> del app.config['TANGO_BUILD_BASE']
    >>> build_static_site(app)
    Traceback (most recent call last):
        ...
    ConfigurationError: app config is missing TANGO_BUILD_BASE
    >>> import os
    >>> _ = os.system('rm -fr public/')
    >>>
    """
    if output is None:
        sitepath = app.config.get('TANGO_BUILD_DIR') or 'public'
        if not app.config.has_key('TANGO_BUILD_BASE'):
            raise ConfigurationError('app config is missing TANGO_BUILD_BASE')
        output = app.config['TANGO_BUILD_BASE'] + '/' + sitepath
    # Ensure output directory is an absolute path.
    output = os.path.abspath(output)
    app.config['FREEZER_DESTINATION'] = output
    app.config['TANGO_BUILD_DIR'] = app.config['FREEZER_DESTINATION']
    if not os.path.exists(output):
        os.makedirs(output)
    freezer = Freezer(app)
    freezer.register_generator(build_endpoint_routing(app))
    freezer.freeze()
    return app


def build_endpoint_routing(app):
    """Build endpoint routing as needed for Frozen-Flask url generation.

    >>> from tango.factory import build_app
    >>> app = build_app('testsite')
    >>> url_generator = build_endpoint_routing(app)
    >>> for endpoint, keywords in url_generator():
    ...     print endpoint, keywords
    /another/<argument>/ {'argument': 3}
    /another/<argument>/ {'argument': 4}
    /another/<argument>/ {'argument': 5}
    /files/page-<parameter>.html {'parameter': 0}
    /files/page-<parameter>.html {'parameter': 1}
    /files/page-<parameter>.html {'parameter': 2}
    /routing/<parameter>/ {'parameter': 0}
    /routing/<parameter>/ {'parameter': 1}
    /routing/<parameter>/ {'parameter': 2}
    >>>
    """
    def routing():
        for route in app.routes:
            for argument, values in route.routing.items():
                for value in values:
                    yield route.rule, {argument: value}
    return routing
