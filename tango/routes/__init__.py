"Package to parse & handle routes declared by a Tango site."

def prefix(head, *paths):
    """Prefix sequence of strings with given head, for URL route declaration.

    >>> prefix('/figures/numbers/', 'one', 'two', 'three')
    ('/figures/numbers/one', '/figures/numbers/two', '/figures/numbers/three')
    >>> prefix('/path/', '', 'to/another')
    ('/path/', '/path/to/another')
    >>>
    """
    return tuple(head + path for path in paths)


def get_routes(app):
    """Get app routes from app's site package routes module.

    >>> from tango.app import Tango
    >>> get_routes(Tango('testsite')) # doctest: +NORMALIZE_WHITESPACE
    {'index.html': ('/',),
     'parameter.html': ('/routing/<parameter>/',
                        '/files/page-<parameter>.html'),
     'argument.html': ('/another/<argument>/',)}
    >>>
    """
    return __import__(app.import_name+'.routes', fromlist=['routes']).routes
