"""Tango mobile web optimization framework."""

from setuptools import setup, find_packages

from tango.manage import version

setup(
    name='Tango',
    version=version.number,
    url='http://www.willowtreeapps.com',
    description='mobile web optimization framework',
    long_description=__doc__,
    maintainer=version.maintainer,
    maintainer_email=version.maintainer_email,
    packages=find_packages(),
    namespace_packages=['tango', 'tango.site'],
    install_requires=[
        'Flask',
        ],
    entry_points={
        'console_scripts': [
            'tango = tango.manage:run'
            ],
        },
    tests_require=[
        'nose',
        'minimock',
        ],
    test_suite='nose.collector',
    )
