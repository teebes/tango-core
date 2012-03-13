"""
site: gists
routes:
 - json: /
exports:
 - description: A collection of gists from rduplain.
 - gists
"""

# Quickstart, in the root tango-core directory:
#
#     python setup.py develop
#     pip install requests
#     cd examples
#     tango serve gists # in one terminal
#     tango shelve gists # in another, shelves to /tmp/tango.db.

import requests
import json

gist_list_url = 'https://api.github.com/users/rduplain/gists'
gist_detail_url_format = 'https://api.github.com/gists/%s'

gists = []
for gist_obj in json.loads(requests.get(gist_list_url).text):
    gist = {}
    for key in ('description', 'created_at', 'git_pull_url'):
        gist[key] = gist_obj[key]
    gist_detail_url = gist_detail_url_format % gist_obj['id']
    gist['files'] = json.loads(requests.get(gist_detail_url).text)['files']
    gists.append(gist)
