#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'requests==2.10.0',
    'asciimatics==1.6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='quickprompts',
    version='0.0.1',
    description="A utility for common tasks of prompting users for data.",
    long_description=readme + '\n\n' + history,
    author="Justin Staubach",
    author_email='justin@staubach.us',
    url='https://github.com/JEStaubach/quickprompts',
    packages=[
        'quickprompts',
    ],
    package_dir={'quickprompts':
                 'quickprompts'},
    entry_points={
        'console_scripts': [
            'quickprompts=quickprompts.quickprompts:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='quickprompts',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
