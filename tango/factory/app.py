"Package to instantiate a Tango object from a Tango stash module."

from flask import request
from werkzeug import create_environ

from tango.app import Tango
from tango.imports import module_exists, module_is_package
from tango.imports import package_submodule, namespace_segments
import tango
import tango.filters

from tango.factory.context import build_module_routes
from tango.factory.snapshot import get_snapshot


def get_app(import_name, **options):
    """Get a Tango app object from a site by the given import name.

    This function looks for an object named app in the package or module
    matching the import name provided by the given argument, and if it does not
    exist, builds an app from the stash inside the package or module.

    Hybrid apps, those with both stash and dynamic views, start with an app
    built from stash, then extend the app through the Flask API.

    >>> get_app('simplesite') # doctest:+ELLIPSIS
    <tango.app.Tango object at 0x...>
    >>> get_app('testsite') # doctest:+ELLIPSIS
    <tango.app.Tango object at 0x...>
    >>> get_app('simplest') # doctest:+ELLIPSIS
    <tango.app.Tango object at 0x...>
    >>>

    Here's a simple app which has both a stash and app additions:
    >>> app = get_app('hybrid')
    >>> app # doctest:+ELLIPSIS
    <tango.app.Tango object at 0x...>
    >>> app.this_was_added_after_stash
    'Hello, world!'
    >>>
    """
    if module_is_package(import_name):
        # This if-condition helps avoid importing single-module sites.
        module = __import__(import_name)
        # Prefer app defined in module over a newly built app from site stash.
        app = getattr(module, 'app', None)
        if app is not None:
            return app
    # Build the app if a single-module site, or no app is found in package.
    return build_app(import_name, **options)


def build_app(import_name, import_stash=False, use_snapshot=True,
              report_file=None):
    """Create a Tango application object from a Python import name.

    This function accepts three kinds of import names:

    1. a single module name where the module is itself a stash
    2. a package name which has a submodule or sub-package named 'stash'.
    3. a dotted module name referring to a module inside a package's stash.

    In case #1, the module is a self-contained application in one .py file.

    In case #2, the package is arbitrarily laid out, but the stash module
    inside it is one or more modules conforming to Tango's stash conventions.

    In case #3, the module is inside a package matching case #2, but the import
    name refers to a module which by itself would otherwise match case #1.
    Case #3 is treated like case #1 with one important exception.  Since the
    module is inside a package, that package is used as the application
    object's import name for the purposes of loading configuration directives,
    as stash modules are allowed to and encouraged to use their projects
    config.py.  This is essential to shelving modules in isolation when working
    with a stash package with more than one stash module.

    Example, using the a single module called simplest.py (case #1):
    >>> app = build_app('simplest')
    >>> app.url_map # doctest:+NORMALIZE_WHITESPACE
    Map([[<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
          <Rule '/' (HEAD, OPTIONS, GET) -> />]])
    >>>

    Example, using the simplesite module in this project (case #2):
    >>> app = build_app('simplesite')
    >>> app.url_map # doctest:+NORMALIZE_WHITESPACE
    Map([[<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
          <Rule '/' (HEAD, OPTIONS, GET) -> />]])
    >>>

    Example, using submodule in the stash in a package with config (case #3):
    >>> app = build_app('simplesite.stash.index')
    >>> app.url_map # doctest:+NORMALIZE_WHITESPACE
    Map([[<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
          <Rule '/' (HEAD, OPTIONS, GET) -> />]])
    >>>

    Example, using submodule in the stash in a package without config
    (case #3 but identical to case #1):
    >>> app = build_app('testsite.stash.package.module')
    >>> app.url_map # doctest:+NORMALIZE_WHITESPACE
    Map([[<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
          <Rule '/index.json' (HEAD, OPTIONS, GET) -> /index.json>]])
    >>>
    """
    # Initialize application. See docstring above for construction logic.
    app = None
    package_name, module_name = package_submodule(import_name)
    if package_name and module_name:
        # import_name points to submodule, look for package config.
        root_package_name = namespace_segments(import_name)[0]
        if module_exists(root_package_name + '.config'):
            app = Tango(root_package_name)
            app.config.from_object(root_package_name + '.config')

    if app is None:
        app = Tango(import_name)

    # Check for a site config.
    if module_exists(import_name + '.config'):
        app.config.from_object(import_name + '.config')

    # Create app context, push it onto request stack for use in initialization.
    ctx = app.request_context(create_environ())
    ctx.push()

    # Load Tango filters.
    # Only needed for packages; single modules do not have implicit templates.
    if module_is_package(import_name):
        tango.filters.init_app(app)

    # Build application routes, checking for a snapshot first.
    routes = None
    if use_snapshot:
        routes = get_snapshot(import_name)

    if routes is None:
        build_options = {'import_stash': import_stash}
        build_options['report_file'] = report_file
        if module_exists(import_name + '.stash'):
            module = __import__(import_name, fromlist=['stash']).stash
            routes = build_module_routes(module, **build_options)
        else:
            routes = build_module_routes(import_name, **build_options)
    else:
        print 'Using snapshot with stashed template context.'
    app.routes = routes

    # Stitch together context, template, and path.
    for route in app.routes:
        app.build_view(route)

    # Pop app request context.
    ctx.pop()

    app.context_processor(lambda: request.view_args)
    return app
