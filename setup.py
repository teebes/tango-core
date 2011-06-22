"""Tango mobile web optimization framework."""

import sys

from setuptools import setup, find_packages

# Avoid importing tango here, to get accurate test coverage reports.
# Test tango sites reside in the tests/ directory.
sys.path.append('tests')
sys.path.append('tests/errors')


setup(
    name='Tango',
    version='0.1',
    url='http://www.willowtreeapps.com',
    license='Commercial',
    author='Ron DuPlain',
    author_email='ron.duplain@willowtreeapps.com',
    description=__doc__,
    long_description=open('README.rst').read(),
    packages=find_packages(),
    platforms=['POSIX'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'distribute',
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
