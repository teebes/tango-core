"Utilities for internal use within Tango framework."


def package_submodule(hierarchical_module_name):
    """Provide package name, submodule name from dotted module name.

    Example:
    >>> package_submodule('tango.site.default')
    ('tango.site', 'default')
    >>> package_submodule('tango.site')
    ('tango', 'site')
    >>> package_submodule('tango')
    (None, 'tango')
    >>> package_submodule('')
    (None, None)
    >>>
    """
    tokens = hierarchical_module_name.split('.')
    return str('.'.join(tokens[:-1])) or None, str(tokens[-1]) or None


def get_module(name):
    """Get a module given its import name.

    This is particularly useful since Python's imp.find_module does not handle
    hierarchical module names (names containing dots).

    Example:
    >>> get_module('tango.site.default.content') # doctest:+ELLIPSIS
    <module 'tango.site.default.content' from '...'>
    >>> get_module('tango.site.default') # doctest:+ELLIPSIS
    <module 'tango.site.default' from '...'>
    >>> get_module('tango.site') # doctest:+ELLIPSIS
    <module 'tango.site' from '...'>
    >>> get_module('tango') # doctest:+ELLIPSIS
    <module 'tango' from '...'>
    >>>
    """
    packagename, base = package_submodule(name)
    if packagename is None:
        return __import__(base)
    return getattr(__import__(packagename, fromlist=[base]), base)
