"Marshal template contexts exported declaratively by Tango content packages."

import pkgutil

import yaml


HINT_DELIMITER = '<-'


def build_site_context(package):
    """Pull contexts from site package, discovering modules & parsing headers.

    Structure of site context:

    site_context = {'site': {'path1': {}, 'path2': {}, 'pathN': {}}}
    site_context['site']['pathN'] is a standard template context dict.

    >>> import tango.site.default.content
    >>> build_site_context(tango.site.default.content)
    ... # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    {'default': {'/path1': {'count': 2, 'name': '...', 'sequence': [4, 5, 6]},
    '/path2': {'count': 2, 'name': '...', 'sequence': [4, 5, 6]},
    '/': {'project': 'tango', 'hint': '...', 'title': '...'}}}
    >>>

    :param package: Tango site content package object
    :type package: module
    """
    site_context = {}

    for module in discover_modules(package):
        context = pull_context(module)
        if context is None:
            continue
        for sitekey in context:
            site = site_context.get(sitekey, {})
            for pathkey in context[sitekey]:
                path = site.get(pathkey, {})
                # TODO: Warn on path context overwrite.
                path.update(context[sitekey][pathkey])
                site[pathkey] = path
            site_context[sitekey] = site
    return site_context


def discover_modules(package):
    """Discover content package modules, returning iterable of module objects.

    This searches all subpackages and includes __init__ modules.

    Example:
    >>> import tango.site.default.content
    >>> discover_modules(tango.site.default.content) # doctest:+ELLIPSIS
    <generator object discover_modules at 0x...>
    >>> list(discover_modules(tango.site.default.content))
    ... # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [<module 'tango.site.default.content' from '...'>,
     <module 'tango.site.default.content.index' from '...'>,
     <module 'tango.site.default.content.multiple' from '...'>,
     <module 'tango.site.default.content.package' from '...'>,
     <module 'tango.site.default.content.package.module' from '...'>]
    >>>

    :param package: Tango site content package object
    :type package: module
    """
    path = package.__path__
    prefix = package.__name__ + '.'
    onerror = lambda args: None
    yield package
    for _, name, _ in pkgutil.walk_packages(path, prefix, onerror):
        tokens = name.split('.')
        packagename = '.'.join(tokens[:-1])
        base = tokens[-1]
        module = getattr(__import__(packagename, fromlist=[base]), base)
        yield module


def pull_context(module):
    """Pull dict template context from module, parsing it's header.

    Example:
    >>> from tango.site.default.content import index, multiple
    >>> pull_context(index)
    {'default': {'/': {'title': 'MobileTango Starter'}}}
    >>> pull_context(multiple) # doctest:+NORMALIZE_WHITESPACE
    {'default': {'/path1': {'count': 2, 'name': 'multiple.py context',
    'sequence': [4, 5, 6]}, '/path2': {'count': 2, 'name':
    'multiple.py context', 'sequence': [4, 5, 6]}}}
    >>>

    :param module: Tango site content package module object
    :type module: module
    """
    header = parse_header(module)
    if header is None:
        return None

    path_context = {}
    for name in header['export']:
        path_context[name] = getattr(module, name)

    site_context = {}
    for path in header['path']:
        site_context[path] = path_context

    return {header['site']: site_context}


def parse_header(module):
    """Parse module header for template context metadata.

    Modules in the site content package must have these fields in the header:

    * site
    * path
    * export

    Raise KeyError if any of these fields are missing.

    Example:
    >>> from tango.site.default.content import index, multiple
    >>> parse_header(index)
    {'path': ['/'], 'export': {'title': 'string'}, 'site': 'default'}
    >>> header = parse_header(multiple)
    >>> header['site']
    'default'
    >>> header['path']
    ['/path1', '/path2']
    >>> header['export']
    {'count': 'number', 'name': 'string', 'sequence': '[number]'}
    >>>

    :param module: Tango site content package module object
    :type module: module
    """
    try:
        rawheader = yaml.load(module.__doc__)
    except yaml.scanner.ScannerError:
        # TODO: Warn about failed parse here, reporting module.__name__.
        return None
    except AttributeError:
        # Not an error or a warning, just a module without a docstring.
        return None

    if not isinstance(rawheader, dict):
        # module has a docstring, but it's not yaml.
        return None

    header = {'site': rawheader['site']}

    if isinstance(rawheader['path'], basestring):
        header['path'] = [rawheader['path']]
    else:
        header['path'] = list(rawheader['path'])
        # TODO: Warn about duplicates here, reporting module.__name__.

    header['export'] = {}
    if isinstance(rawheader['export'], basestring):
        rawexport = [rawheader['export']]
    else:
        rawexport = list(rawheader['export'])
    for exportstmt in rawexport:
        # TODO: Warn about duplicates here, reporting module.__name__.
        try:
            name, hint = [x.strip() for x in exportstmt.split(HINT_DELIMITER)]
            header['export'][name] = hint
        except ValueError:
            # TODO: Warn of bad export, reporting exportstmt, module.__name__.
            continue

    return header
