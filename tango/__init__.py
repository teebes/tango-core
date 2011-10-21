from email.utils import formataddr

from flask import abort, request, session

import app
import config
import errors
import factory
import imports
import tools


__all__ = ['abort', 'errors', 'request', 'session', 'app', 'build', 'config',
           'factory', 'imports', 'tools',
           '__codename__', '__fullversion__', '__label__']


# Keep this codename up-to-date; it's useful in common language.
__codename__ = 'Salida'


# Keep this maintainer contact up to date, it's used in a version label.
__maintainer__ = "Ron DuPlain"
__email__ = "ron.duplain@willowtreeapps.com"


# Append yourself to author, chronological order.
# Add yourself to credits, alphabetical by first name.
__author__ = 'Ron DuPlain and Matt Dawson'
__copyright__ = 'Copyright 2010-2011, WillowTree Apps, Inc.'
__credits__ = ['Matt Dawson',
               'Ron DuPlain',
               "Thibaud Morel l'Horset",
               ]


# Derive version metadata from the distribution, to allow version labels to be
# maintained in one place within this project.  Version will be UNKNOWN if
# parsing the version from the distribution fails for any reason.
# This project depends on 'distribute' to provide pkg_resources.
try:
    __version__ = __import__('pkg_resources').get_distribution('Tango').version
except Exception:
    __version__ = 'UNKNOWN'


def build_fullversion(version, codename):
    return 'Tango {0} {1}'.format(codename, version)


def build_contact(name, email):
    return formataddr((name, email))


def build_label(fullversion, contact):
    return '{0}\nMaintainer: {1}'.format(fullversion,contact)


# Construct a labels for use in displaying tango framework meta info.
__fullversion__ = build_fullversion(__version__, __codename__)
__contact__ = build_contact(__maintainer__, __email__)
__label__ = build_label(__fullversion__, __contact__)
