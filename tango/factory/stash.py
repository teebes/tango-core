"Shelve an application's stash."

from tango.factory import build_app


def shelve(import_name):
    app = build_app(import_name, import_stash=True, use_snapshot=False)
    for route in app.routes:
        app.connector.put(route.site, route.rule, route.context)

