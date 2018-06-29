from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='Mopidy-Redbox',
    version=get_version('mopidy_redbox/__init__.py'),
    url='https://github.com/lukhe/mopidy-redbox',
    license='Apache License, Version 2.0',
    author='Vivien HENRY',
    author_email='vivien.henry@outlook.fr',
    description='Mopidy Extension for Redbox project',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 1.0',
        'Pykka >= 1.1',
        'pyzmq',
	'pyserial'
    ],
    entry_points={
        'mopidy.ext': [
            'redbox = mopidy_redbox:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
