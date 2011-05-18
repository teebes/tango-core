Testing: Package Metadata
=========================

Verify a version string is available.

>>> import tango
>>> tango.__version__ # doctest:+ELLIPSIS
'...'
>>> tango.__version__ != 'UNKNOWN'
True
>>>


Verify version is UNKNOWN, but still available if pkg_resources is not.
Specifically, break the import mechanics.  This may seem like great lengths,
but this project depends on pkg_resources carefully.  Expand this test should
issues arise across packaging utilities.

>>> import __builtin__
>>> global base_import
>>> base_import = __builtin__.__import__
>>> def broken_import(*args, **kwargs):
...     if args[0] == 'pkg_resources':
...         raise ImportError
...     return base_import(*args, **kwargs)
>>> __builtin__.__import__ = broken_import
>>> reload(tango) # doctest:+ELLIPSIS
<module 'tango' from '...'>
>>> tango.__version__
'UNKNOWN'
>>> __builtin__.__import__ = base_import
>>> reload(tango) # doctest:+ELLIPSIS
<module 'tango' from '...'>
>>>
