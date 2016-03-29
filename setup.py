#!/usr/bin/env python

from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='eventortoolkit',
    version='0.1',
    description='Interface for easier use of eventor API.',
    long_description=long_description,
    author='Jonathan Anderson',
    author_email='jonathan@jonathananderson.se',
    license='MIT',
    url='https://github.com/andersonjonathan/Eventor-toolkit',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='Eventor orienteering development',
    py_modules=['eventortoolkit'],
    install_requires=[
        'requests',
        'xmltodict'
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
