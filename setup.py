#!/usr/bin/env python

from setuptools import setup

setup(
    name='Eventor-toolkit',
    version='0.1',
    description='Interface for easier use of eventor API.',
    author='Jonathan Anderson',
    author_email='jonathan@jonathananderson.se',
    url='https://github.com/andersonjonathan/Eventor-toolkit',
    install_requires=[
        'requests',
        'xmltodict'
    ],
)
