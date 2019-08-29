#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'Readme.md')).read()

setup(name='gitutils',
      version='1.4.4',
      description="GITUTILS is a tool to facilitate the server-side operations when developing software that uses git repositories.",
      long_description=README,
      author='Paul Scherrer Institute (PSI)',
      url='https://git.psi.ch/controls_highlevel_applications/app_config',
      packages=['gitutils'],
      )
