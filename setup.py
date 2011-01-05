"""Tango mobile web optimization framework."""

from setuptools import setup, find_packages

setup(
    name='Tango',
    version='0.0',
    description='mobile web optimization framework',
    long_description=__doc__,
    packages=find_packages(),
    namespace_packages=['tango', 'tango.site'],
    install_requires=[
        ],
    tests_require=[
        'nose',
        'minimock',
        ],
    test_suite='nose.collector',
    )
