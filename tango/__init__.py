from flask import abort, request, session

import app
import build
import config
import factory
import helpers
import routes
import tools


__all__ = ['abort', 'request', 'session', 'app', 'build', 'config', 'factory',
           'helpers', 'routes', 'tools']


# Derive version metadata from the distribution, to allow version labels to be
# maintained in one place within this project.  Version will be UNKNOWN if
# parsing the version from the distribution fails for any reason.
# This project depends on 'distribute' to provide pkg_resources.
try:
    __version__ = __import__('pkg_resources').get_distribution('Tango').version
except Exception:
    __version__ = 'UNKNOWN'
