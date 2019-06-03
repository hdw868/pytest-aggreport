#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-aggreport',
    version='0.1.0',
    author='Wayne Hong',
    author_email='hdw868@126.com',
    maintainer='Wayne Hong',
    maintainer_email='hdw868@126.com',
    license='MIT',
    url='https://github.com/hdw868/pytest-aggreport',
    description='pytest plugin for pytest-repeat that aggregates test result of the same test in terminal and html(if pytest-html is available).',
    long_description=read('README.rst'),
    packages=['pytest_aggreport'],
    package_data={'pytest_aggreport': ['resources/*']},
    python_requires='>=3.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['pytest>=4.3.1', 'beautifultable>=0.7.0', 'py>=1.8.0', 'pytest-repeat>=0.8.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'aggreport = pytest_aggreport.plugin',
        ],
    },
)
