# -*- coding: utf-8 -*-
from os.path import join, dirname
from setuptools import setup, find_packages
import sys
import os

VERSION = (3, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

f = open(join(dirname(__file__), 'README.md'))
long_description = f.read().strip()
f.close()

install_requires = [
]


setup(
    name = 'tsl2561',
    description = "Driver for the TSL2561 digital luminosity (light) sensors",
    license = "BSD",
    url = "https://github.com/sim0nx/tsl2561",
    download_url = "https://github.com/sim0nx/tsl2561",
    long_description = long_description,
    version = __versionstr__,
    author = "Georges Toth",
    author_email = "georges@trypill.org",
    packages = find_packages(
        where='.',
    ),
    keywords = ['TSL2561'],
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=install_requires,
)
