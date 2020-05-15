#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='hasty',
    version='0.0.1',
    install_requires=[
        'requests',
        'pyperclip',
    ],
    extras_require={
        'testing': [
            'pytest',
            'responses'
        ],
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    package_data={
        # If any package contains *.ini files, include them
        '': ['*.ini'],
    },
    url='https://github.com/Vikdemen/hasty',
    license='MIT License',
    author='Demenev Viktor',
    author_email='viktor.demen@gmail.com',
    description='Python-based hastebin CLI client',
    entry_points={
        'console_scripts': ['hasty = hasty.__main__:main']
    }
)
