"""Version information for Tango mobile web optimization framework.

On major version release of Tango, set ``notice`` to '' and distribute.
Immediately after release:

* Bump ``number``.
* Set ``name`` to a new tango codename.
* Set ``notice`` to 'dev'.

Approaching release, distribute upon setting ``notice`` to release status:

* 'dev' is the head/tip of development, prior to alpha release
* 'a': alpha -- 'a', 'a1', 'a2', ...
* 'b': beta -- 'b', 'b1', 'b2', ...
* 'c': candidate release -- 'c', 'c1', 'c2', ...

Bump number or letter immediately after an alpha/beta/candidate release.

On a maintenance release or backport:

* Set ``number`` as appropriate.
* Set ``name`` to tango codename matching major version number.
* Set ``notice`` to ''.

Update maintainer and maintainer_email as soon as project changes hands.
"""


class Version(object):
    "Version management class for flexibility in project versioning metadata."
    number = '0.1'
    name = 'Basico'
    notice = 'dev'
    maintainer = 'Ron DuPlain'
    maintainer_email = 'ron.duplain@willowtreeapps.com'

    @property
    def dist(self):
        if self.notice:
            return self.number + self.notice
        return self.number

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
