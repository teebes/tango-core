"Marshal template contexts exported declaratively by Tango stash modules."

import pkgutil
import warnings

import yaml

from tango.app import Route
from tango.errors import DuplicateContextWarning, DuplicateExportWarning
from tango.errors import DuplicateRouteWarning, DuplicateRoutingWarning
from tango.errors import HeaderException
from tango.helpers import get_module, module_is_package
from tango.helpers import url_parameter_match


def build_module_routes(module, context=True, routing=True):
    """Pull contexts from a Tango stash, discovering modules & parsing headers.

    Returns list of Route objects with attributes via structured docstrings.

    >>> import testsite.stash
    >>> build_module_routes(testsite.stash)
    ... # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [<Route: /, template:index.html>,
     <Route: /another/<argument>/, template:argument.html>,
     <Route: /blank/export.txt>,
     <Route: /blank/routing.txt>,
     <Route: /files/page-<parameter>.html, template:parameter.html>,
     <Route: /index.json, json>,
     <Route: /norouting/<parameter>/, template:parameter.html>,
     <Route: /plain/<routing>.txt, text>,
     <Route: /plain/exports.txt, text>,
     <Route: /route1.txt>,
     <Route: /route2.txt>,
     <Route: /routing/<parameter>/, template:parameter.html>]
    >>>

    :param module: Tango site stash module object
    :type module: module
    :param context: flag whether to pull template contexts into route objects
    :param routing: flag whether to pull routing iterables into route objects
    """
    route_collection = []

    for module in discover_modules(module):
        module_routes = parse_header(module)
        if not module_routes:
            continue
        if context:
            module_routes = pull_context(module_routes)
        if routing:
            module_routes = pull_routing(module_routes)
        route_collection += module_routes

    route_table = {}
    for route in route_collection:
        if route.rule in route_table:
            route_context = route_table[route.rule].context
            new_route_context = route.context

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


def discover_modules(module):
    """Discover stash modules, returning iterable of module objects.

    Note that both packages and modules result in module objects.
    This searches all subpackages and includes __init__ modules.

    Example:
    >>> import testsite.stash
    >>> discover_modules(testsite.stash) # doctest:+ELLIPSIS
    <generator object discover_modules at 0x...>
    >>> list(discover_modules(testsite.stash))
    ... # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [<module 'testsite.stash' from '...'>,
     <module 'testsite.stash.index' from '...'>,
     <module 'testsite.stash.multiple' from '...'>,
     <module 'testsite.stash.package' from '...'>,
     <module 'testsite.stash.package.module' from '...'>]
    >>>

    Modules are supported in addition to packages.
    >>> import testsite.stash.index
    >>> list(discover_modules(testsite.stash.index)) # doctest:+ELLIPSIS
    [<module 'testsite.stash.index' from '...'>]
    >>>

    :param module: Tango site stash module object
    :type module: module
    """
    yield module
    if module_is_package(module):
        prefix = module.__name__ + '.'
        for _, name, _ in pkgutil.walk_packages(module.__path__, prefix):
            yield get_module(name)


def pull_context(route_objs):
    """Pull dict template context from module using Routes parsed from header.

    Examples:
    >>> from testsite.stash import index
    >>> routes = pull_context(parse_header(index))
    >>> routes
    [<Route: /, template:index.html>]
    >>> routes[0].context
    {'title': 'Tango'}
    >>>

    >>> from testsite.stash import multiple
    >>> routes = pull_context(parse_header(multiple))
    >>> routes
    [<Route: /route1.txt>, <Route: /route2.txt>]
    >>> routes[0].context == routes[1].context
    True
    >>> routes[0].context
    {'count': 2, 'name': 'multiple.py context', 'sequence': [4, 5, 6]}
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


def pull_routing(route_objs):
    """Pull routing iterables from module using Routes parsed from header.

    Examples:
    >>> from testsite.stash import index
    >>> routes = pull_routing(parse_header(index))
    >>> routes
    [<Route: /, template:index.html>]
    >>> routes[0].routing_exports
    {}
    >>> routes[0].routing
    {}
    >>>

    >>> from testsite.stash import routing
    >>> routes = pull_routing(parse_header(routing))
    >>> len(routes)
    3
    >>> routes[0].rule
    '/another/<argument>/'
    >>> routes[0].routing
    {'argument': xrange(3, 6)}
    >>> routes[1].rule
    '/files/page-<parameter>.html'
    >>> routes[1].routing
    {'parameter': [0, 1, 2]}
    >>> routes[2].rule
    '/routing/<parameter>/'
    >>> routes[2].routing
    {'parameter': [0, 1, 2]}
    >>>

    >>> pull_routing([]) is None
    True
    >>> pull_routing(None) is None
    True
    >>>

    :param route_objs: list of Route instances, provided by parse_header
    """
    if route_objs is None or len(route_objs) == 0:
        return None

    # All route objects from a module have same exports, but diff routing.
    routing = {}

    for route_obj in route_objs:
        assert len(route_obj.modules) == 1, "I'm confused by multiple modules."
        module = get_module(route_objs[0].modules[0])
        route_obj.routing = {}
        for param in route_obj.routing_exports:
            if routing.has_key(param):
                route_obj.routing[param] = routing[param]
            else:
                name = route_obj.routing_exports[param]
                param_iterable = getattr(module, name)
                route_obj.routing[param] = param_iterable
                routing[param] = param_iterable

    return route_objs


def parse_header(module):
    """Parse module header for template context metadata.

    Modules in the site stash must have these fields in the header:

    * site
    * routes
    * exports

    Raise KeyError if any of these fields are missing.
    Raise HeaderException if header is not pure yaml.
    Return None if module has no docstring or defines no routes.

    Examples:
    >>> from testsite.stash import index
    >>> routes = parse_header(index)
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

    >>> from testsite.stash import multiple
    >>> routes = parse_header(multiple)
    >>> routes
    [<Route: /route1.txt>, <Route: /route2.txt>]
    >>> [route.site for route in routes]
    ['test', 'test']
    >>> routes[0].exports == routes[1].exports
    True
    >>> routes[0].exports
    {'count': None, 'name': None, 'sequence': None}
    >>>

    >>> from testsite.stash.package import module
    >>> routes = parse_header(module)
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

    >>> from testsite.stash import routing
    >>> routes = parse_header(routing)
    >>> routes # doctest:+NORMALIZE_WHITESPACE
    [<Route: /another/<argument>/, template:argument.html>,
     <Route: /files/page-<parameter>.html, template:parameter.html>,
     <Route: /routing/<parameter>/, template:parameter.html>]
    >>> routes[0].routing_exports
    {'argument': 'arguments'}
    >>> routes[1].routing_exports
    {'parameter': 'parameters'}
    >>> routes[2].routing_exports
    {'parameter': 'parameters'}
    >>> routes[0].site == routes[1].site == routes[2].site == 'test'
    True
    >>> routes[0].exports == routes[1].exports == routes[2].exports
    True
    >>> routes[0].exports # doctest:+ELLIPSIS
    {'purpose': '...'}
    >>> routes[0].static == routes[1].static == routes[2].static
    True
    >>> routes[0].static
    ['purpose']
    >>>

    >>> import testsite.stash.package
    >>> parse_header(testsite.stash.package) is None
    True
    >>>

    >>> from testsite.stash import dummy
    >>> parse_header(dummy) is None
    True
    >>>

    >>> from errorsite.stash import hybrid
    >>> parse_header(hybrid)
    Traceback (most recent call last):
      ...
    HeaderException: metadata docstring must be yaml or doc, but not both.
    >>>

    :param module: Tango site stash module object
    :type module: module
    """
    try:
        header = yaml.load(module.__doc__)
    except yaml.scanner.ScannerError:
        raise HeaderException('metadata docstring must be yaml or doc, '
                              'but not both.')
    except AttributeError:
        # Not an error or a warning, just a module without a docstring.
        return None

    if not isinstance(header, dict):
        # module has a docstring, but it's not yaml.
        return None

    # Relevant values to pull from header, of various types.
    site = header['site']
    rawroutes = header['routes']
    exports = {}
    rawexports = header['exports']
    routing_exports = {}
    rawrouting = header.get('routing', [])
    static = []

    # Ensure an iterable on raw values.
    if rawroutes is None:
        rawroutes = []
    if rawexports is None:
        rawexports = []
    if rawrouting is None:
        rawrouting = []

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
            msg = msg.format(module.__name__, name)
            warnings.warn(msg, DuplicateExportWarning)
        exports[name] = value
    static = list(export_static_names)

    # Test for and warn on routing export duplicates while constructing dict.
    for export_dict in rawrouting:
        if not export_dict:
            continue
        url_parameter, export_variable = export_dict.items()[0]
        if routing_exports.has_key(url_parameter):
            msg = '{0} duplicate routing export: {1}'
            msg = msg.format(module.__name__, name)
            warnings.warn(msg, DuplicateRoutingWarning)
        routing_exports[url_parameter] = export_variable

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
            msg = msg.format(module.__name__, route)
            warnings.warn(msg, DuplicateRouteWarning)
        route_obj = Route(site, route, exports, static, template)
        route_obj.modules = [module.__name__]
        route_obj.routing_exports = {}
        for param in routing_exports:
            if url_parameter_match(route, param):
                route_obj.routing_exports[param] = routing_exports[param]
        route_table[route] = route_obj

    return sorted(route_table.values(), key=lambda route: route.rule)
