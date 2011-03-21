"Package to build a Tango site into a collection of static files."

from os.path import abspath, dirname
import os

from flaskext.frozen import Freezer


def build_static_site(app):
    # TODO: Provide a better default output directory. (Basico)
    build_path = dirname(dirname(abspath(__file__))) + '/output'
    app.config['FREEZER_DESTINATION'] = build_path
    if not os.path.exists(build_path):
        os.makedirs(build_path)
    ctx = app.package_context
    # TODO: Register routing directives with the freezer. (Basico)
    # TODO: Check if routing directive is a callable. (Basico)
    # TODO: Wrap routing iterable/generator to holdback None values. (Basico)
    freezer = Freezer(app)
    freezer.freeze()
    return app
