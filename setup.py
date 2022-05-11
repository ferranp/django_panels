#!/usr/bin/env python
import os
from distutils.core import setup

__author__ = u'Ferran Pegueroles'
__copyright__ = u'Copyright 2022, Ferran Pegueroles'
__credits__ = [u'Ferran Pegueroles']


__license__ = 'BSD'
__version__ = '0.1'
__email__ = 'ferran@pegueroles.com'


long_description = ""

setup(
    name='django_panels',
    version=__version__,
    url='https://bitbucket.org/ferranp/django_panels/',
    author=__author__,
    author_email=__email__,
    license='GPL',
    packages=[
        'panels',
        'panels.migrations',
              ],
    description='Panels for django',
    long_description=long_description,
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Topic :: Internet :: WWW/HTTP :: Dynamic Content']
)
