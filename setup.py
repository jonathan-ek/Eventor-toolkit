#!/usr/bin/env python

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Eventor-toolkit',
    version='1.0.4',
    description='Interface for easier use of eventor API.',
    long_description=long_description,
    author='Jonathan Anderson',
    author_email='jonathan@jonathananderson.se',
    license='MIT',
    url='https://github.com/andersonjonathan/Eventor-toolkit',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

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
    py_modules=['eventor_toolkit'],
    install_requires=[
        'requests',
        'xmltodict'
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
