#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='easygui_qt',
    version='0.1.0',
    description='"Inspired by easygui, designed for PyQt"',
    long_description=readme + '\n\n' + history,
    author='André Roberge',
    author_email='andre.roberge@gmail.com',
    url='https://github.com/aroberge/easygui_qt',
    packages=[
        'easygui_qt',
    ],
    package_dir={'easygui_qt':
                 'easygui_qt'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='easygui_qt',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Students and teachers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
