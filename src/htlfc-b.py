#!/usr/bin/env python3
"""A wrapper to launch HyperText Legacy File Converter
for conversion and display in browser (for testing)."""

import sys
from htlfc import main

if __name__ == '__main__':
    sys.exit(main.call_browser())
