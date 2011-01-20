"Console entry point and management & development tasks for Tango framework."


class Version(object):
    "Version management class for flexibility in project versioning metadata."
    number = '0.1'
    name = 'Basico'
    notice = 'dev' # Set to '' on release.
    maintainer = 'Ron DuPlain'
    maintainer_email = 'ron.duplain@willowtreeapps.com'

    @property
    def banner(self):
        return 'Tango %(number)s (%(name)s) %(notice)s' % type(self).__dict__

    @property
    def maintainer_info(self):
        return ('Maintainer: %(maintainer)s <%(maintainer_email)s>'
                % type(self).__dict__)

    @property
    def label(self):
        return '%s\n%s' % (self.banner, self.maintainer_info)


info = Version()