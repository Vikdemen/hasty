#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='hasty',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    url='----',
    license='MIT License',
    author='Demenev Viktor',
    author_email='viktor.demen@gmail.com',
    description='Python-based hastebin CLI client',
    entry_points={
        'console_scripts': ['hasty = hasty.hasty:main']
    }
)
