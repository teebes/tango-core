"""Tango mobile web optimization framework."""

import sys

from setuptools import setup, find_packages

from tango import version


# Test tango sites reside in the tests/ directory.
sys.path.append('tests')


setup(
    name='Tango',
    version=version.info.dist,
    url='http://www.willowtreeapps.com',
    description='mobile web optimization framework',
    long_description=__doc__,
    maintainer=version.info.maintainer,
    maintainer_email=version.info.maintainer_email,
    packages=find_packages(),
    license='Commercial',
    platforms=['POSIX'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'BeautifulSoup',
        'Flask',
        'Flask-Script',
        'Frozen-Flask',
        'lxml',
        'pyyaml',
        ],
    entry_points={
        'console_scripts': [
            'tango = tango.manage:run'
            ],
        },
    tests_require=[
        'nose',
        'minimock==1.2.5',
        'Flask-Testing',
        ],
    test_suite='nose.collector',
    )
