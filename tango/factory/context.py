"Marshal template contexts exported declaratively by Tango content packages."

import pkgutil

import yaml


def build_site_context(package):
    "Pull contexts from site package, discovering modules & parsing headers."


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
    "Pull dict template context from module, parsing it's header."


def parse_header(module):
    "Parse module header for template context metadata."
