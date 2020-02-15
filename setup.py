# -*- coding: utf-8 -*-
from os.path import join, dirname

import setuptools

with open(join(dirname(__file__), 'README.rst')) as fhdl:
    long_description = fhdl.read().strip()

setuptools.setup(
    name='tsl2561',
    description="Driver for the TSL2561 digital luminosity (light) sensors",
    license="BSD",
    url="https://github.com/sim0nx/tsl2561",
    download_url="https://github.com/sim0nx/tsl2561",
    long_description=long_description,
    version='3.4.0',
    author="Georges Toth",
    author_email="georges@trypill.org",
    packages=setuptools.find_packages(),
    install_requires=['Adafruit_GPIO'],
    package_data={'tsl2561': ['py.typed']},
    zip_safe=False,
    python_requires='>=3.5',
    keywords=['TSL2561'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3 :: Only',
    ]
)
