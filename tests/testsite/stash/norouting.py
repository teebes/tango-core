"""
site: test
routes:
 - parameter.html: /norouting/<parameter>/
exports:
 - purpose: Show that empty route iterables are okay.
routing:
 - parameter: parameters
"""

parameters = []
