#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'Readme.md')).read()

setup(name='app_config',
      version='1.3.2',
      description="Configuration management tools to support configuration change workflows",
      long_description=README,
      author='Paul Scherrer Institute (PSI)',
      url='https://git.psi.ch/git_tools/git_workflow_tools',
      packages=['app_config'],
      # package_dir={'app_config': 'src'},
      # package_data={'pylauncher': ['resources/images/*.png', 'resources/qss/*.qss', 'resources/mapping/*.json']},
      # platforms=["any"],
      )
