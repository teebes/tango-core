"Package to build a Tango site into a collection of static files."

import os

from flaskext.frozen import Freezer


def build_static_site(app, path=None):
    if path is None:
        sitepath = app.config['SITE'] or 'build'
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
