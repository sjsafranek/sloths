#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = 'sloths',
    version = '0.0.1',
    description = 'Provides metadata about fields within delimited files',
    author = 'Stefan Safranek',
    author_email = 'sjsafranek@gmail.com',
    url = '',
    install_requires = [
        'pandas>=1.2.0'
    ],
    python_requires = '!=2.*, >=3.6',
    packages = ['sloths'],
    package_dir = {'sloths': 'sloths'},
    package_data = {'': ['LICENSE']},
    include_package_data = True,
    license = 'MIT',
    zip_safe = True,
    entry_points={'console_scripts': ['sloths = sloths.__main__:main']},
)
