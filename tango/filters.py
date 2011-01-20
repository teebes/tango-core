from flask import current_app


filters = {}


def init_app(app):
    "Load filters registered in this module onto given app object."
    app.jinja_env.filters.update(filters)
    return app


def register(f):
    "Decorator to register given function to load onto app via init_app."
    filters[f.__name__] = f
    return f


def get_default(key):
    "Get a default value from the current app's configuration."
    try:
        app = current_app
    except AttributeError:
        return None
    return app.config[key]
