"""Tango mobile web optimization framework."""

import sys

from setuptools import setup, find_packages

# Avoid importing tango here, to get accurate test coverage reports.
# Test tango sites reside in the tests/ directory.
sys.path.append('tests')
sys.path.append('tests/errors')


setup(
    name='Tango',
    version='0.2',
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
        'BeautifulSoup<4.0',
        'Flask<0.8', # Skip 0.8 for 0.9. Flask 0.8 imports in app constructor.
        'Flask-Script>0.3.1',
        'lxml',
        'pytest',
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
    dependency_links=[
        'http://pypi:a0nyZbjtFanl@cherry.willowtreeapps.com/pypi/index/Flask-Script/',
        ],
    )
