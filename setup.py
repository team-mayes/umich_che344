#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'scipy',
    'matplotlib', 'numpy', 'six',
]

test_requirements = [
]

setup(
    name='umich_che344',
    version='0.1.0',
    description="Handy Python scripts for ChE344",
    long_description=readme + '\n\n' + history,
    author="Heather Mayes",
    author_email='hbmayes@umich.edu',
    url='https://github.com/hmayes/umich_che344',
    packages=[
        'umich_che344',
    ],
    package_dir={'umich_che344':
                 'umich_che344'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='umich_che344',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
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
