"Attempt to load and run Flask testsuite when this module is run as main."

import unittest


if __name__ == '__main__':
    # flask.testsuite added to Flask August 2011.
    try:
        from flask.testsuite import BetterLoader, suite; suite
        unittest.main(testLoader=BetterLoader(), defaultTest='suite')
    except ImportError:
        print 'Unable to find flask.testsuite.'
