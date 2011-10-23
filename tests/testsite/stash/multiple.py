"""
site: test
routes:
 - /route1.txt
 - /route2.txt
exports:
 - name
 - count
 - purpose: Push the same set of exports to multiple routes.
 - sequence
"""

name = 'multiple.py context'
count = 2
sequence = [4, 5, 6]
