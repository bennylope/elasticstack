#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import elasticstack

version = elasticstack.__version__

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='elasticstack',
    version=version,
    description="""Configurable indexing and other extras for Haystack (with ElasticSearch biases).""",
    long_description=readme + '\n\n' + history,
    author='Ben Lopatin',
    author_email='ben@wellfire.co',
    url='https://github.com/bennylope/elasticstack',
    packages=[
        'elasticstack',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.4',
        'django-haystack>=2.0.0',
    ],
    license="BSD",
    zip_safe=False,
    keywords='elasticstack',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
