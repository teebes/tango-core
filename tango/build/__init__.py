"Package to build a Tango site into a collection of static files."

from os.path import abspath, dirname
import os

from flaskext.frozen import Freezer


def build_static_site(app):
    build_path = dirname(dirname(abspath(__file__))) + '/output'
    app.config['FREEZER_DESTINATION'] = build_path
    if not os.path.exists(build_path):
        os.makedirs(build_path)
    ctx = app.package_context
    freezer = Freezer(app)
    freezer.freeze()
    return app
