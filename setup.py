#!/usr/bin/env python
# coding=utf-8

from setuptools import setup
from pympris import __version__, __description__, requires, README


setup(name='pympris',
      version=__version__,
      description=__description__,
      author='Mikhail Mamrouski',
      author_email='wst.public.mail@gmail.com',
      url="https://github.com/wistful/pympris",
      license="MIT License",
      packages=['pympris'],
      long_description=README,
      install_requires=requires,
      test_suite='tests.convert_test',
      platforms=["Unix,"],
      keywords="mpris, dbus",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: X11 Applications",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      )
