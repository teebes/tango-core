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

    >>> from tango.factory import create_app
    >>> get_routes(create_app('tango.site.default'))
    {'index.html': ('/',)}
    >>>
    """
    return __import__(app.import_name+'.routes', fromlist=['routes']).routes
