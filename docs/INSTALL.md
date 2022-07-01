# Installation
Hypertext Legacy File Converter "HTLFC" is a Python 3 application hosted on GitHub.
Most people would install HTLFC with the *PIP Method* although the *Manual Method* is described first.

## Manual Method
Use this method to download and test HTLFC without a permanent installation.

### Prerequisites
HTLFC requires Python version 3.6 or later.
Check your version:

    $ python
    >>> import sys
    >>> sys.version

In addition to the Python standard library, HTLFC also requires the following modules:

    >>> import lxml
    >>> import chardet

If any of the above fail, install them through either your Operating System package manager or with `pip3`.

### Fetch HTLFC

Complete one of the following:

#### ZIP File
From the HTLFC repository on GitHub, pull down the options under the **Code** button and select *Download ZIP*.  Unzip the result to a working directory on your computer.

#### GIT Clone
Ensure that `git` is installed in your Operating System.

Start by creating a working directory on your computer. Then clone the repository:

    $ git clone https://github.com/HairySpoon/htlfc.git

### Execute HTLFC in Place

Under the working directory created above, go to the `src/` sub-directory.
Validate the executable:

    $ ./htlfc.py -h

To complete your evaluation of HTLFC, try any of the following:
>* Launch `htlfc.py` as above, provide a full path to `infile` and `outfile`.
>* Starting at the location of `infile`, launch `htlfc.py` using a full path.
>* Launch `htflc.py -g` and select files through the data entry form.

## PIP Method
Use this method to install HTLFC into your `PYTHONPATH` so that it may be invoked from anywhere.

Ensure that `pip3` version 18.1 or later is installed:

    $ pip3 -V

### From GitHub

    $ pip3 install git+https://github.com/HairySpoon/htlfc.git

### Execute
Validate the executable; start in any directory and...

    $ htlfc.py -h

Usage instructions appear in the `README.md` file in the repository on GitHub.
