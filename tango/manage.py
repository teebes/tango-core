"Console entry point and management & development tasks for Tango framework."

class Version(object):
    "Version management class for flexibility in project versioning metadata."
    number = '0.1'
    name = 'Basico'
    notice = 'dev' # Set to '' on release.
    maintainer = 'Ron DuPlain'
    maintainer_email = 'ron.duplain@willowtreeapps.com'

    @property
    def label(self):
        return ('Tango %(number)s (%(name)s) %(notice)s\n'
                'Maintainer: %(maintainer)s <%(maintainer_email)s>'
                % type(self).__dict__)

version = Version()


def run():
    print "Not yet implemented."
