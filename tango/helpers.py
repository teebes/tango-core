"Utilities for internal use within Tango framework."

import imp
import pkgutil
import re
import types


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


def get_module_docstring(filepath):
    """Get module-level docstring of Python module at filepath.

    Get the docstring without running the code in the module, therefore
    avoiding any side-effects in the file. This is particularly useful for
    scripts with docstrings.

    A filepath string is used instead of module object to avoid side-effects.

    Example:
    >>> filepath = get_module_filepath('testsite.stash.index')
    >>> filepath # doctest:+ELLIPSIS
    '.../tests/testsite/stash/index.py'
    >>> print get_module_docstring(filepath).strip()
    site: test
    routes:
     - template:index.html: /
    exports:
     - title: Tango
    >>>

    Example, module without a docstring:
    >>> print get_module_docstring(get_module_filepath('empty'))
    None
    >>>
    """
    co = compile(open(filepath).read(), filepath, 'exec')
    if co.co_consts and isinstance(co.co_consts[0], basestring):
        docstring = co.co_consts[0]
    else:
        docstring = None
    return docstring


def get_module_filepath(module_or_name):
    """Get the file path of the given module, or None if a name & not found.

    Example, using modules:
    >>> import testsite # a Python package
    >>> import simplest # a single .py module
    >>> get_module_filepath(testsite) # doctest:+ELLIPSIS
    '...tests/testsite'
    >>> 'tests/simplest.py' in get_module_filepath(simplest)
    True
    >>>


    Example, using import names:
    >>> get_module_filepath('testsite.stash') # doctest:+ELLIPSIS
    '.../tests/testsite/stash'
    >>> get_module_filepath('testsite.stash.index') # doctest:+ELLIPSIS
    '.../tests/testsite/stash/index.py'
    >>> get_module_filepath('simplest') # doctest:+ELLIPSIS
    '.../tests/simplest.py'
    >>> get_module_filepath('doesnotexist')
    >>>
    """
    if isinstance(module_or_name, types.ModuleType):
        module = module_or_name
        if hasattr(module, '__path__'):
            # A package's __path__ attribute is a list. Use the first element.
            return module.__path__[0]
        else:
            return module.__file__
    else:
        name = module_or_name
        try:
            loader = pkgutil.get_loader(name)
        except ImportError:
            return None
        if loader is None:
            return None
        else:
            return loader.filename


def discover_modules(module_or_name):
    """Given an import name, provide an iterable of module filepath,name pairs.

    This function imports package __init__.py but does not import modules.

    More specifically, given a package name, this function walks the package
    (which requires importing the package __init__) and yields the filepath and
    name of each module (as a tuple of strings) in the package.  Python treats
    both packages and modules as module objects, and this function makes no
    distinction.  Give this function an import name and it returns an iterable
    regardless of whether the import name maps to a package or a module; in the
    case of a module name, the iterable results in only one element.

    Example:
    >>> discover_modules('testsite.stash') # doctest:+ELLIPSIS
    <generator object discover_modules at 0x...>
    >>> for item in discover_modules('testsite.stash'):
    ...     print item # doctest: +ELLIPSIS
    ...
    testsite.stash
    testsite.stash.blank
    testsite.stash.blankexport
    testsite.stash.blankrouting
    testsite.stash.dummy
    testsite.stash.emptyrouting
    testsite.stash.index
    testsite.stash.multiple
    testsite.stash.noexports
    testsite.stash.norouting
    testsite.stash.package
    testsite.stash.package.module
    testsite.stash.routing
    >>> list(discover_modules('testsite.stash.index')) # doctest:+ELLIPSIS
    ['testsite.stash.index']
    >>>

    For flexibility & support, a module may be used in addition to a string.
    >>> import testsite.stash
    >>> discover_modules(testsite.stash) # doctest:+ELLIPSIS
    <generator object discover_modules at 0x...>
    >>> for item in discover_modules(testsite.stash):
    ...     print item # doctest: +ELLIPSIS
    ...
    testsite.stash
    testsite.stash.blank
    testsite.stash.blankexport
    testsite.stash.blankrouting
    testsite.stash.dummy
    testsite.stash.emptyrouting
    testsite.stash.index
    testsite.stash.multiple
    testsite.stash.noexports
    testsite.stash.norouting
    testsite.stash.package
    testsite.stash.package.module
    testsite.stash.routing
    >>> import testsite.stash.index
    >>> list(discover_modules(testsite.stash.index))
    ['testsite.stash.index']
    >>>

    :param module_or_name: Tango site stash import name, or imported module
    :type module_or_name: str
    """
    if isinstance(module_or_name, types.ModuleType):
        module = module_or_name
        name = module.__name__
        yield name
    else:
        module = None
        name = module_or_name
        yield name
    if module_is_package(name):
        if module is None:
            module = get_module(name)
        prefix = name + '.'
        for _, name, _ in pkgutil.walk_packages(module.__path__, prefix):
            yield name


def module_exists(name):
    """Return True if a module by the given name exists, or False if not.

    Example:
    >>> module_exists('doesnotexist')
    False
    >>> module_exists('tango')
    True
    >>> module_exists('simplesite')
    True
    >>> module_exists('simplesite.config')
    True
    >>> module_exists('simplest')
    True
    >>> module_exists('simplest.config')
    False
    >>> module_exists('importerror')
    True
    >>> module_exists('testsite.stash.package.module')
    True
    >>> module_exists('testsite.stash.package.doesnotexist')
    False
    >>> module_exists('doesnotexist.module')
    False
    >>>
    """
    # This function must be very careful not to suppress real ImportErrors.
    package, submodule = package_submodule(name)
    if package is None:
        try:
            imp.find_module(name)
        except ImportError:
            return False
        return True

    root = root_package(package)
    try:
        pkg = imp.find_module(root)
    except ImportError:
        return False

    pkg = __import__(root)
    if not module_is_package(pkg):
        return False
    for _, x, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__+'.'):
        if x == name:
            return True
    return False


def module_is_package(module_or_name):
    """Return True if import name is for a Python package, or False if not.

    Returns None if the package is not found.

    Example, using import names:
    >>> module_is_package('testsite')
    True
    >>> module_is_package('simplest')
    False
    >>> module_is_package('doesnotexist')
    >>>

    Example, using modules:
    >>> import testsite # a Python package
    >>> import simplest # a single .py module
    >>> module_is_package(testsite)
    True
    >>> module_is_package(simplest)
    False
    >>>
    """
    if isinstance(module_or_name, types.ModuleType):
        module = module_or_name
        if hasattr(module, '__path__'):
            return True
        else:
            return False
    else:
        name = module_or_name
        loader = pkgutil.get_loader(name)
        if loader is None:
            return None
        # Provides a simpler interface to loader.is_package(fullname).
        # loader.is_package requires fullname argument, even though it isn't used.
        return loader.etc[2] == imp.PKG_DIRECTORY


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


def root_package(hierarchical_module_name):
    """Provide the root package name from a dotted module name.

    Example:
    >>> root_package('tango.factory')
    'tango'
    >>> root_package('tango.helpers')
    'tango'
    >>> root_package('testsite')
    'testsite'
    >>> root_package('testsite.stash')
    'testsite'
    >>> root_package('testsite.stash.package')
    'testsite'
    >>> root_package('testsite.stash.package.module')
    'testsite'
    >>>
    """
    return hierarchical_module_name.split('.')[0]


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
