"""Tango mobile web optimization framework."""

from setuptools import setup, find_packages

from tango import version


setup(
    name='Tango',
    version=version.info.number,
    url='http://www.willowtreeapps.com',
    description='mobile web optimization framework',
    long_description=__doc__,
    maintainer=version.info.maintainer,
    maintainer_email=version.info.maintainer_email,
    packages=find_packages(),
    # Include package data, disable zipping to allow Jinja2 to find templates.
    include_package_data=True,
    zip_safe=False,
    # tango, tango.site are namespace packages. Others are full packages.
    namespace_packages=['tango', 'tango.site'],
    install_requires=[
        'Flask',
        'Flask-Script',
        'pyyaml',
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
