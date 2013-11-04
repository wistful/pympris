#!/usr/bin/env python
# coding=utf-8

from setuptools import setup
from pympris import __version__, __description__, requires, README


setup(name='pympris',
      version=__version__,
      description=__description__,
      author='Mikhail Mamrouski',
      author_email='wst.public.mail@gmail.com',
      url="https://bitbucket.org/wistful/pympris",
      license="MIT License",
      packages=['pympris'],
      description='pympris uses to control media player using MPRIS2',
      long_description=README,
      install_requires=requires,
      platforms=["Unix,"],
      keywords="mpris, dbus",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: X11 Applications",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      )
