"""Tango mobile web optimization framework."""

from setuptools import setup, find_packages

from tango import version


def find_selected_packages():
    exclude_bases = ('tango.site.test', 'tango.site.importerror')
    excludes = []
    for exclude_base in exclude_bases:
        excludes.append(exclude_base)
        excludes.append(exclude_base + '.*')
    return find_packages(exclude=excludes)


setup(
    name='Tango',
    version=version.info.number,
    url='http://www.willowtreeapps.com',
    description='mobile web optimization framework',
    long_description=__doc__,
    maintainer=version.info.maintainer,
    maintainer_email=version.info.maintainer_email,
    packages=find_selected_packages(),
    # Include package data, disable zipping to allow Jinja2 to find templates.
    include_package_data=True,
    zip_safe=False,
    # tango, tango.site are namespace packages. Others are full packages.
    namespace_packages=['tango', 'tango.site'],
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
        'minimock',
        'Flask-Testing',
        ],
    test_suite='nose.collector',
    )
