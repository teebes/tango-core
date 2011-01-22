"Tools for generating context content from existing (X)HTML documents."

import urllib2

from lxml import etree
from lxml.cssselect import CSSSelector


parser = etree.HTMLParser()


def dict_zip(**kwargs):
    """Return a list of dictionaries from provided iterable keyword arguments.

    Each dictionary returned contains one value, in order, from each provided
    iterable. The key for each value is taken from the key of the iterable from
    which it originated.

    """
    return [dict(zip(kwargs.keys(), item)) for item in zip(*kwargs.values())]


def url_selector(url, selector, text_only=False):
    """Return the unicode representation of an HTML element from `url` matched
    by `selector`.

    If `selector` matches multiple elements, they will be concatenated into a
    single unicode string.

    """
    tree = etree.parse(urllib2.urlopen(url), parser)
    cs = CSSSelector(selector)
    source = u''
    for branch in cs(tree):
        if text_only:
            source += branch.text
        else:
            source += etree.tostring(branch)
    return source


def url_selector_list(url, selector, text_only=False):
    """Return a list of HTML elements from `url` matched by `selector`, converted
    to unicode strings.

    If `text_only` is True, only the text contents of the matched elements are
    included.

    """
    tree = etree.parse(urllib2.urlopen(url), parser)
    cs = CSSSelector(selector)
    if text_only:
        return [branch.text for branch in cs(tree)]
    return [etree.tostring(branch) for branch in cs(tree)]
