"Utilities for internal use within Tango framework."

import re


def get_module(name):
    """Get a module given its import name.

    This is particularly useful since Python's imp.find_module does not handle
    hierarchical module names (names containing dots).

    Example:
    >>> get_module('simplesite.stash') # doctest:+ELLIPSIS
    <module 'simplesite.stash' from '...'>
    >>> get_module('simplesite') # doctest:+ELLIPSIS
    <module 'simplesite' from '...'>
    >>> get_module('testsite') # doctest:+ELLIPSIS
    <module 'testsite' from '...'>
    >>> get_module('tango') # doctest:+ELLIPSIS
    <module 'tango' from '...'>
    >>>
    """
    packagename, base = package_submodule(name)
    if packagename is None:
        return __import__(base)
    return getattr(__import__(packagename, fromlist=[base]), base)


def get_module_filepath(module):
    """Get the file path of the given module.

    Example:
    >>> import testsite # a Python package
    >>> import simplest # a single .py module
    >>> get_module_filepath(testsite) # doctest:+ELLIPSIS
    '...tests/testsite'
    >>> 'tests/simplest.py' in get_module_filepath(simplest)
    True
    >>>
    """
    if hasattr(module, '__path__'):
        # A package's __path__ attribute is a list. Use the first element.
        return module.__path__[0]
    else:
        return module.__file__


def module_is_package(module):
    """Return True if module is a Python package, or False if not.

    Example:
    >>> import testsite # a Python package
    >>> import simplest # a single .py module
    >>> module_is_package(testsite)
    True
    >>> module_is_package(simplest)
    False
    >>>
    """
    if hasattr(module, '__path__'):
        return True
    else:
        return False


def package_submodule(hierarchical_module_name):
    """Provide package name, submodule name from dotted module name.

    Example:
    >>> package_submodule('simplesite')
    (None, 'simplesite')
    >>> package_submodule('tango.factory')
    ('tango', 'factory')
    >>> package_submodule('tango')
    (None, 'tango')
    >>> package_submodule('')
    (None, None)
    >>>
    """
    tokens = hierarchical_module_name.split('.')
    return str('.'.join(tokens[:-1])) or None, str(tokens[-1]) or None


def url_parameter_match(route, parameter):
    """Determine whether a route contains a url parameter, return True if so.

    Example:
    >>> url_parameter_match('/<argument>', 'argument')
    True
    >>> url_parameter_match('/<argument>/', 'argument')
    True
    >>> url_parameter_match('/<int:argument>', 'argument')
    True
    >>> url_parameter_match('/int:<argument>/', 'argument')
    True
    >>> url_parameter_match('/path:<argument>/', 'argument')
    True
    >>> url_parameter_match('/path/to/<parameter>/', 'parameter')
    True
    >>> url_parameter_match('/path/to/<path:parameter>/', 'parameter')
    True
    >>> url_parameter_match('/path/to/<aparameter>/', 'parameter')
    False
    >>> url_parameter_match('/path/to/<path:aparameter>/', 'parameter')
    False
    >>> url_parameter_match('/', 'parameter')
    False
    >>>
    """
    return re.search('[<:]{0}>'.format(parameter), route) is not None
