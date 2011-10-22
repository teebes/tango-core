"Shelve an application's stash."

from sys import stdout

from tango.factory import build_app


def shelve(import_name, report_file=stdout):
    app = build_app(import_name, import_stash=True, use_snapshot=False,
                    report_file=report_file)
    for route in app.routes:
        app.connector.put(route.site, route.rule, route.context)
