#!/usr/bin/env python

# install PyYAML if missing
try:
    import yaml
except:
    from setuptools.command import easy_install
    easy_install.main( ["-U","PyYAML"] )

# the original zenpacklib stuff
from . import zenpacklib

CFG = zenpacklib.load_yaml()
