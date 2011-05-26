"""
site: test
routes:
 - parameter.html:
   - /routing/<parameter>/
   - /files/page-<parameter>.html
 - argument.html:
   - /another/<argument>/
exports:
 - purpose: Show that route parameters are implicitly added to context.
routing:
 - parameter: parameters
 - argument: arguments
"""

# TODO: Build a full test for this site. (Basico)

parameters = range(3) # a list
arguments = xrange(3,6) # a lazy iterable
