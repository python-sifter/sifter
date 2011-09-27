#!/usr/bin/env python

from distutils.core import setup

setup(
        name = "sifter",
        version = "0.1",
        author = "Gary Peck",
        author_email = "gary@realify.com",
        url = "https://github.com/garyp/sifter",
        description = "Parser/evaluator for the Sieve filtering language (RFC 5228)",
        classifiers = [
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "License :: OSI Approved :: BSD License",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Operating System :: OS Independent",
            "Topic :: Communications :: Email :: Filters",
            "Topic :: Software Development :: Interpreters",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ],
        packages = [
            "sifter",
            "sifter.commands",
            "sifter.comparators",
            "sifter.extensions",
            "sifter.grammar",
            "sifter.t",
            "sifter.tests",
            "sifter.validators",
            ],
        package_data = {
            "sifter.t" : ["*.in", "*.out", "*.msg", "*.rules"],
            },
        )

