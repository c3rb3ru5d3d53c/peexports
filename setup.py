#!/usr/bin/env python

import os
from glob import glob
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

__author__  = '@c3rb3ru5d3d53c'
__version__ = '1.0.0'

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='peexports',
    version=__version__,
    maintainer=__author__,
    description='A PE Export Collection Utility',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=open('requirements.txt', 'r').read().splitlines(),
    scripts=['peexports.py'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
)