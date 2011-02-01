"Marshal template contexts exported declaratively by Tango content packages."

import pkgutil

import yaml


HINT_DELIMITER = '<-'


def build_package_context(package):
    """Pull contexts from site package, discovering modules & parsing headers.

    Structure of site context:

    site_context = {'site': {'path1': {}, 'path2': {}, 'pathN': {}}}
    site_context['site']['pathN'] is a standard template context dict.

    >>> import tango.site.test.content
    >>> build_package_context(tango.site.test.content)
    ... # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    {'test': {'/path1': {'count': 2, 'name': '...', 'sequence': [4, 5, 6]},
     '/path2': {'count': 2, 'name': '...', 'sequence': [4, 5, 6]},
     '/': {'project': 'tango', 'hint': '...', 'title': '...'},
     '/routing/<parameter>': {'purpose': '...'}}}
    >>>

    :param package: Tango site content package object
    :type package: module
    """
    package_context = {}

    for module in discover_modules(package):
        context = pull_context(module)
        if context is None:
            continue
        for site in context:
            site_context = package_context.get(site, {})
            for path in context[site]:
                path_context = site_context.get(path, {})
                # TODO: Warn on path context overwrite.
                path_context.update(context[site][path])
                site_context[path] = path_context
            package_context[site] = site_context
    return package_context


def discover_modules(package):
    """Discover content package modules, returning iterable of module objects.

    This searches all subpackages and includes __init__ modules.

    Example:
    >>> import tango.site.test.content
    >>> discover_modules(tango.site.test.content) # doctest:+ELLIPSIS
    <generator object discover_modules at 0x...>
    >>> list(discover_modules(tango.site.test.content))
    ... # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [<module 'tango.site.test.content' from '...'>,
     <module 'tango.site.test.content.index' from '...'>,
     <module 'tango.site.test.content.multiple' from '...'>,
     <module 'tango.site.test.content.package' from '...'>,
     <module 'tango.site.test.content.package.module' from '...'>]
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
    >>> from tango.site.test.content import index, multiple
    >>> pull_context(index)
    {'test': {'/': {'title': 'Tango'}}}
    >>> pull_context(multiple) # doctest:+NORMALIZE_WHITESPACE
    {'test': {'/path1': {'count': 2, 'name': 'multiple.py context',
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
        if name in header['static']:
            path_context[name] = header['export'][name]
        else:
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
    >>> from tango.site.test.content import index, multiple
    >>> parse_header(index) # doctest:+NORMALIZE_WHITESPACE
    {'path': ['/'], 'static': ['title'], 'export': {'title': 'Tango'},
     'site': 'test'}
    >>> header = parse_header(multiple)
    >>> header['site']
    'test'
    >>> header['path']
    ['/path1', '/path2']
    >>> header['export']
    {'count': 'number', 'name': 'string', 'sequence': '[number]'}
    >>> from tango.site.test.content.package import module
    >>> parse_header(module)
    {'path': ['/'], 'static': [], 'export': {'hint': None}, 'site': 'test'}
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
    header['static'] = []
    if isinstance(rawheader['export'], basestring):
        rawexport = [rawheader['export']]
    else:
        rawexport = list(rawheader['export'])
    for exportstmt in rawexport:
        # TODO: Warn about duplicates here, reporting module.__name__.
        if isinstance(exportstmt, basestring):
            tokens = exportstmt.split(HINT_DELIMITER)
            name = tokens[0].strip()
            if len(tokens) > 1:
                hint = HINT_DELIMITER.join(tokens[1:]).strip()
                header['export'][name] = hint
            else:
                header['export'][name] = None
        else:
            for name in exportstmt:
                header['export'][name] = exportstmt[name]
                header['static'].append(name)
    return header
