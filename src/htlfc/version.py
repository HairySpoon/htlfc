#!/usr/bin/env python3
"""The file VERSION in this directory, is kept current by GitHub workflows.
It is read directly by setuptools in pyproject.toml
get_version() is called from main()
"""
import os

def get_version():
    root = os.path.split(__file__)[0]
    vers_file = os.path.join(root, "VERSION")
    with open(vers_file,'r') as fp:
        version = fp.readline()
    return version
