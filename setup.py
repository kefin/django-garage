"""
setup.py

Setup.py for django-garage.

Copyright (c) 2012-2013 kevin chan <kefin@makedostudio.com>

* created: 2013-01-12 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-01-12 kchan
"""

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name = "django-garage",
    version = "0.1.0",
    packages = ['garage'],
    include_package_data = True,
    license = "BSD",
    description = "A collection of useful functions and modules for Django development",
    long_description = README,
    url = "https://bitbucket.org/kchan",
    author = "Kevin Chan",
    author_email = "kefin@makedostudio.com",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    install_requires = [
        'django',
        'markdown',
        'textile',
        'PIL',
        'pyyaml',
        ]
)
