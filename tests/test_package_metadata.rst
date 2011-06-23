Testing: Package Metadata of tango package
==========================================

Verify a version string is available.

>>> import tango
>>> tango.__version__ # doctest:+ELLIPSIS
'...'
>>> tango.__version__ != 'UNKNOWN'
True
>>>


Verify version is UNKNOWN, but still available if pkg_resources is not.
Specifically, temporarily override pkg_resources in sys.modules to trigger an
ImportError on ``import pkg_resources``.  This may seem like great lengths, but
this project depends on pkg_resources carefully.  Expand this test should
issues arise across packaging utilities.

>>> import sys
>>> import pkg_resources
>>> sys.modules['pkg_resources'] = None
>>> reload(tango) # doctest:+ELLIPSIS
<module 'tango' from '...'>
>>> tango.__version__
'UNKNOWN'
>>> sys.modules['pkg_resources'] = pkg_resources
>>> reload(tango) # doctest:+ELLIPSIS
<module 'tango' from '...'>
>>>
