# Installation
Hypertext Legacy File Converter "HTLFC" is a Python 3 application, it may be installed either manually or through `pip3`.

## Manual Method
Use this method to download and test HTLFC without a permanent installation.  Also relevant for software development.

### Prerequisites
HTLFC requires Python version 3.6 or later.
Check your version:

    $ python
    >>> import sys
    >>> sys.version

In addition to the Python standard library, HTLFC requires these modules:

    >>> import lxml
    >>> import chardet

If any of the above fail, install the missing modules, either through your Operating System's package manager or with `pip3`.

### Fetch HTLFC

Complete one of the following:

#### ZIP File
From the HTLFC repository on GitHub, pull down the options under the **Code** button and select *Download ZIP*.  Unzip the result to a working directory on your computer.

#### GIT Clone
Ensure that `git` is installed in your Operating System.

Create a working directory on your computer; then clone the repository:

    $ git clone https://github.com/HairySpoon/htlfc.git

### Execute HTLFC in Place

Under the working directory created above, go to the `src/` sub-directory.
Validate the executable:

    $ ./htlfc.py -h

To continue your evaluation of HTLFC, try any of the following:
>* Launch `htlfc.py` as above, provide a full path to `infile` and `outfile`.
>* Starting at the location of `infile`, launch `htlfc.py` using a full path.
>* Launch `htflc.py -g` and select files through the data entry form.

## PIP Method
Use this method to install HTLFC into your operating system.  Pip will also install the entry point `htlfc` in your executable path.

Ensure that `pip3` version 18.1 or later is installed:

    $ pip3 -V

### From Local Repository
If you followed the manual method above, HTLFC can be installed from the working directory (not `src`) as follows:

    $ pip3 install .

### From GitHub
To install HTLFC without making a working copy do this...

    $ pip3 install git+https://github.com/HairySpoon/htlfc.git


### Execute
Validate the executable.  Launch `htlfc` (without the `.py` extension) from anywhere...

    $ htlfc -h

### Instructions
User documentation consists of the `README.md` file in the GitHub repository.
