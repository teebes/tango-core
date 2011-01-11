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
