"""Entry point used by setuptools to create the executables"""

from htlfc import main

def run_htlfc():
    main.main()

def run_htlfc_b():
    main.call_browser()

