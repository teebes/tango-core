"Marshal template contexts exported declaratively by Tango stash modules."

import warnings

import yaml

from tango.app import Route
from tango.errors import DuplicateContextWarning, DuplicateExportWarning
from tango.errors import DuplicateRouteWarning, HeaderException
from tango.errors import ModuleNotFound
from tango.imports import discover_modules, get_module
from tango.imports import get_module_filepath, get_module_docstring


def build_module_routes(module_or_name, import_stash=False, logfile=None):
    """Discover modules & parse headers from a Tango stash import name.

    Returns list of Route objects with attributes via structured docstrings.

    >>> build_module_routes('testsite.stash')
    ... # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [<Route: /, template:index.html>,
     <Route: /argument/<argument>/, template:argument.html>,
     <Route: /blank/export.txt>,
     <Route: /index.json, json>,
     <Route: /plain/exports.txt, text>,
     <Route: /route1.txt>,
     <Route: /route2.txt>]
    >>>

    :param import_name: Tango site stash import name
    :type import_name: str
    :param context: flag whether to pull template contexts into route objects
    """
    route_collection = []

    for name in discover_modules(module_or_name):
        module_routes = parse_header(name)
        if not module_routes:
            continue
        if import_stash:
            if logfile is not None:
                logfile.write('Loading {0} ... '.format(name))
                # Flush log file to keep user posted on what is processing;
                # otherwise no guarantee that anything is displayed in the
                # log file until an implicit flush.
                logfile.flush()
            module_routes = pull_context(module_routes)
            if logfile is not None:
                logfile.write('done.\n')
        route_collection += module_routes

    route_table = {}
    for route in route_collection:
        # Currently, routes can be defined in multiple stash modules.
        # Check to see if the route is already loaded and check for collisions.
        if route.rule in route_table:
            route_context = route_table[route.rule].context or {}
            new_route_context = route.context or {}

            # Test for and warn on route context override.
            current_keys = set(route_context.keys())
            new_keys = set(new_route_context.keys())
            intersection = current_keys.intersection(new_keys)
            if intersection:
                msg = '{0} duplicate context, exports: {1}'
                msg = msg.format(route, ', '.join(intersection))
                warnings.warn(msg, DuplicateContextWarning)
            route_context.update(new_route_context)
            route.context = route_context
            route.modules += route_table[route.rule].modules

        route_table[route.rule] = route
    return sorted(route_table.values(), key=lambda route: route.rule)


def pull_context(route_objs):
    """Pull dict template context from module using Routes parsed from header.

    Examples, when using this function directly:
    >>> routes = pull_context(parse_header('testsite.stash.index'))
    >>> routes
    [<Route: /, template:index.html>]
    >>> routes[0].context
    {'title': 'Tango'}
    >>>

    >>> routes = pull_context(parse_header('testsite.stash.multiple'))
    >>> routes
    [<Route: /route1.txt>, <Route: /route2.txt>]
    >>> routes[0].context == routes[1].context
    True
    >>> routes[0].context # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    {'count': 2,
     'purpose': '...',
     'name': 'multiple.py context',
     'sequence': [4, 5, 6]}
    >>>

    >>> pull_context([]) is None
    True
    >>> pull_context(None) is None
    True
    >>>

    :param route_objs: list of Route instances, provided by parse_header
    """
    if route_objs is None or len(route_objs) == 0:
        return None

    # All route objects from a module have same exports.
    exports = route_objs[0].exports
    static = route_objs[0].static

    assert len(route_objs[0].modules) == 1, "I'm confused by multiple modules."
    module = get_module(route_objs[0].modules[0])

    context = {}
    for name in exports:
        if name in static:
            context[name] = exports[name]
        else:
            context[name] = getattr(module, name)
    for route_obj in route_objs:
        route_obj.context = context

    return route_objs


def parse_header(import_name):
    """Parse docstring of module matching import name, for stash metadata.

    Modules in the site stash must have these fields in the header:

    * site
    * routes
    * exports

    Return None if module has no docstring or does not appear to be metadata.
    Raise KeyError if any of these fields are missing.
    Raise HeaderException if header is yaml but not pure yaml.

    Examples:
    >>> routes = parse_header('testsite.stash.index')
    >>> routes
    [<Route: /, template:index.html>]
    >>> route = routes[0]
    >>> route.exports
    {'title': 'Tango'}
    >>> route.static
    ['title']
    >>> route.site
    'test'
    >>> route.context
    >>>

    >>> routes = parse_header('testsite.stash.package.module')
    >>> routes
    [<Route: /index.json, json>]
    >>> route = routes[0]
    >>> route.site
    'test'
    >>> route.exports
    {'hint': None}
    >>> route.static
    []
    >>>

    >>> routes = parse_header('testsite.stash.multiple')
    >>> routes
    [<Route: /route1.txt>, <Route: /route2.txt>]
    >>> routes[0].site == routes[1].site
    True
    >>> routes[0].exports == routes[1].exports
    True
    >>> routes[0].exports # doctest:+ELLIPSIS
    {'count': None, 'sequence': None, 'name': None, 'purpose': '...'}
    >>> routes[0].static == routes[1].static
    True
    >>> routes[0].static
    ['purpose']
    >>>

    >>> parse_header('testsite.stash.package') is None
    True
    >>>

    >>> parse_header('testsite.stash.dummy') is None
    True
    >>>

    >>> parse_header('errorsite.stash.hybrid')
    Traceback (most recent call last):
      ...
    HeaderException: metadata docstring must be yaml or doc, but not both.
    >>>

    >>> parse_header(None)
    >>>

    >>> parse_header('doesnotexist')
    Traceback (most recent call last):
      ...
    ModuleNotFound: 'doesnotexist' cannot be found
    >>>

    :param import_name: dotted name of Tango site stash module
    :type import_name: str
    """
    if import_name is None:
        return None

    filepath = get_module_filepath(import_name)
    if filepath is None:
        raise ModuleNotFound("'{0}' cannot be found".format(import_name))

    doc = get_module_docstring(filepath)
    if doc is None:
        return None

    try:
        header = yaml.load(doc)
    except yaml.scanner.ScannerError:
        raise HeaderException('metadata docstring must be yaml or doc, '
                              'but not both.')

    if not isinstance(header, dict):
        # module has a docstring, but it's not yaml.
        return None

    # Relevant values to pull from header, of various types.
    site = header['site']
    rawroutes = header['routes']
    exports = {}
    rawexports = header['exports']
    static = []

    # Ensure an iterable on raw values.
    if rawroutes is None:
        rawroutes = []
    if rawexports is None:
        rawexports = []

    # Coerce routes into a list.
    if isinstance(rawroutes, basestring):
        rawroutes = [rawroutes]
    else:
        rawroutes = list(rawroutes)

    # Coerce exports into a list.
    if isinstance(rawexports, basestring):
        rawexports = [rawexports]
    else:
        rawexports = list(rawexports)

    # Collect export names and static values.
    export_items = []
    export_static_names = set()
    for exportstmt in rawexports:
        if exportstmt is None:
            continue
        if isinstance(exportstmt, basestring):
            # Export statement does not have a static value.
            name = exportstmt
            export_items.append((name, None))
        else:
            # Export statement resulted in a dict of name-to-static exports.
            for name in exportstmt:
                export_items.append((name, exportstmt[name]))
                export_static_names.add(name)

    # Test for and warn on export duplicates while constructing exports dict.
    for item in export_items:
        name, value = item
        if exports.has_key(name):
            msg = '{0} duplicate export: {1}'
            msg = msg.format(import_name, name)
            warnings.warn(msg, DuplicateExportWarning)
        exports[name] = value
    static = list(export_static_names)

    # Build out list of Route instances.
    routes_templates = []
    for rawroute in rawroutes:
        if isinstance(rawroute, dict):
            # routes directive is a map of one template to one or more routes.
            assert len(rawroute) == 1, 'map only one template at a time'
            template = rawroute.keys()[0]
            if isinstance(rawroute[template], basestring):
                # One route.
                routes_templates.append((rawroute[template], template))
            else:
                # Many routes.
                for route in rawroute[template]:
                    routes_templates.append((route, template))
        else:
            # route directive is a route without a template
            routes_templates.append((rawroute, None))

    # Test for and warn on route duplicates while constructing Route objects.
    route_table = {}
    for route, template in routes_templates:
        if route in route_table:
            msg = '{0} duplicate route: {1}'
            msg = msg.format(import_name, route)
            warnings.warn(msg, DuplicateRouteWarning)
        route_obj = Route(site, route, exports, static, template)
        route_obj.modules = [import_name]
        route_table[route] = route_obj

    return sorted(route_table.values(), key=lambda route: route.rule)
