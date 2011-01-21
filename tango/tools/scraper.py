"Tools for generating context content from existing (x)HTML documents."

import urllib2

from lxml import etree
from lxml.cssselect import CSSSelector


parser = etree.HTMLParser()


def url_selector(url, selector):
    """Returns the unicode representation of an HTML element from `url` matched
    by `selector`.

    If `selector` returns multiple elements, they will be concatenated into a
    single unicode string.

    """
    tree = etree.parse(urllib2.urlopen(url), parser)
    cs = CSSSelector(selector)
    source = u''
    for branch in cs(tree):
        source += etree.tostring(branch)
    return source


def url_selector_list(url, selector):
    """Returns a list of HTML elements from `url` matched by selector, converted
    to unicode strings.

    """
    tree = etree.parse(urllib2.urlopen(url), parser)
    cs = CSSSelector(selector)
    return [etree.tostring(branch) for branch in cs(tree)]
