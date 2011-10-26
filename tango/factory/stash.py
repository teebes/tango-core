"Shelve an application's stash."

from tango.app import Tango
from tango.factory.app import build_app


def shelve(app_or_name, logfile=None):
    """Shelve the route contexts of an app, given by object or import name.

    Does not return anything, and inherently has side-effects:
    >>> shelve('simplest')
    >>> shelve(build_app('simplest'))
    """
    if isinstance(app_or_name, Tango):
        app = app_or_name
    else:
        app = build_app(app_or_name, import_stash=True, use_snapshot=False,
                        logfile=logfile)
    for route in app.routes:
        site, rule, context = route.site, route.rule, route.context
        if logfile is not None:
            logfile.write('Stashing {0} {1} ... '.format(site, rule))
        app.connector.put(site, rule, context)
        if logfile is not None:
            logfile.write('done.\n')
