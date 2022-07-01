# Hypertext Legacy File Converter
---
Hypertext Legacy File Converter "HTLFC" converts the following file types into a single `.html` file:

* `.maff` - Mozilla Archive File Format, as produced by the Firefox extension of the same name.
* `.mht` - MIME Hypertext.
* `.war` - Web ARchive as produced by the KDE Konqueror web browser (other sources of `.war` files have not been tested).
* `file+dir` - web page saved as *filename*.html plus *filename_files/* directory (the native "Save As" format used by Firefox and Chrome).

## Use Cases

The original use case for HTLFC emerged when Mozilla discontinued their legacy API; essential to the Firefox MAFF extension which thus became obsolete. Some users were left with collections of `.maff` and `.mht` files which could no longer be opened in the absence of that extension.

Obviously HTLFC may also be used to open and/or convert hypertext files from other sources.

## Principle of Operation
HTLFC performs two fundamental steps:

* The input file is first unpacked into a temporary directory.  Some adjustment may take place depending on the format.
* Associated files (style sheets, images, javascript, etc) are converted into in-line format and merged into the main file.

The user may examine the unpacked content between the two steps.  Use either `--pause` option from the command line, or select "Unpack and  Open Browser" from the graphical interface.

## Usage
These instructions describe invocation of HTLFC simply as `htlfc.py`.  Depending on the user's environment, it may be necessary to include the full path to the executable.

### Command Line
Try this from the command line:

>`htlfc.py infile outfile`

Where `infile` is one of the supported hypertext formats and (the optional) `outfile` will contain the result of conversion.

If `outfile` were not specified, then the result would be saved to `infile.html` - unless `infile.html` represented `file+dir` format, then it's output filename would be mangled to avoid overwriting the input.

Useful command line options:
>`-h | --help` - brief usage summary.

>`-p | --pause` - examine the input after unpack.

### Browser
To examine the unpacked `infile` with the default browser of your operating system:

>`htlfc --browser infile`

>`htlfc -b infile`

Hint: rather than permanently converting your archived hypertext files, create a file association in your operating system, between `htlfc.py -b` and each of the supported file types. When opening one of these files in your file manager, HTLFC will launch your browser with the unpacked file.

### Graphical User Interface
Select your input and output files through a graphical dialogue:

>`htlfc.py --gui`

>`htlfc.py -g`

This interface offers an assisted workflow whereby HTLFC will look for all files under a specified directory.  Then, for each file found, the user may:

  * examine the unpacked file in default browser,
  * examine result of conversion also in browser,
  * convert the input and save output to new file,
  * optionally delete the input file,
  * copy the input file's timestamp to the output.

## Product

### Installation
Follow the instructions at [INSTALL.md](INSTALL.md)

### License
HTLFC is licensed under AGLPv3 in accordance with the file "LICENSE.txt" in the root directory of the source tree.  Choice of license is explained at [AboutLicense](AboutLicense.md)

### Contributing
The developer does not expect to grow the product.  However, contributions to that end are welcome as described in [CONTRIBUTING](CONTRIBUTING.md)


