#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='xswizard',
    version='0.1',
    description='XenServer API wrapper',
    author='Shinya Okano',
    author_email='tokibito@gmail.com',
    url='https://bitbucket.org/tokibito/xswizard/',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Plugins',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['xswizard'],
    #test_suite='tests',
)
