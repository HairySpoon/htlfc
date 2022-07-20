#!/usr/bin/env python3
"""A wrapper to launch HyperText Legacy File Converter
from this directory (for testing)."""

import sys
from htlfc import main

if __name__ == '__main__':
    sys.exit(main.main())
