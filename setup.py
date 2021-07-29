#!/usr/bin/env python

# This file enables editable installs (pip install -e .[dev])

import site
import sys
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

import setuptools

if __name__ == "__main__":
    setuptools.setup()
