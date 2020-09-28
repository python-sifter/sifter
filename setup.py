#!/usr/bin/env python

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="sifter",
    version="0.2.0",
    author="Gary Peck, Manfred Kaiser",
    author_email="gary@realify.com, manfred.kaiser@logfile.at",
    url="https://github.com/garyp/sifter",
    license="BSD",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    project_urls={
        'Source': 'https://github.com/garyp/sifter',
        'Tracker': 'https://github.com/garyp/sifter/issues',
    },
    python_requires='>= 3.6',
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email :: Filters",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=[
        "sifter",
        "sifter.commands",
        "sifter.comparators",
        "sifter.extensions",
        "sifter.grammar",
        "sifter.t",
        "sifter.tests",
        "sifter.validators",
    ],
    package_data={
        "sifter": ['py.typed'],
        "sifter.t": ["*.in", "*.out", "*.msg", "*.rules"],
    },
)
