"""
site: warningsite
routes:
 - /some/route/1/
 - /some/route/2/
exports:
 - hello: world
 - duplicate: export
 - language
 - duplicate: overwrite
 - another
"""

language = 'Python'
another = 'export in this module'
