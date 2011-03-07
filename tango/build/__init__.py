"Package to build a Tango site into a collection of static files."

from flaskext.frozen import Freezer


def build_static_site(app):
    ctx = app.package_context
    freezer = Freezer(app)
    freezer.freeze()
    return app.import_name
