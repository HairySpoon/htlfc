# Hypertext Legacy File Converter
---
Hypertext Legacy File Converter "HTLFC" converts the following file types into a single `.html` file:

* `.maff` - Mozilla Archive File Format, as produced by the Firefox extension of the same name.
* `.mht` - MIME Hypertext.
* `.war` - Web ARchive as produced by the KDE Konqueror web browser (other sources of `.war` files have not been tested).
* `file+dir` - web page saved as *filename*.html plus *filename_files/* directory (the native "Save As" format provided by Firefox and Chrome).

## Use Cases

The original use case for HTLFC emerged when Mozilla discontinued their legacy API; essential to the Firefox MAFF extension which thus became obsolete. Some users were left with collections of `.maff` and `.mht` files which could no longer be opened in the absence of that extension.

Obviously HTLFC may also be used to open and/or convert hypertext files from other sources.

## Principle of Operation
HTLFC makes two passes:

* Pass 1. The input file is unpacked into a temporary directory.  Some adjustment may take place depending on the format.
* Pass 2. Associated files (style sheets, images, javascript, etc) are converted into in-line format and merged (in memory) then written back to storage as one `.html` file.

The user may examine the unpacked content between passes.  Use either `--pause` option from the command line, or select "Unpack and  Open Browser" from the graphical interface.

### Known Limitations
Nested iframes can only be in-lined two levels deep. The first level is enclosed in double quotes ( " ) within this, the second level is enclosed in single quotes ( ' ). Should a file contain a third level, an error will be reported without generating any output. This does not apply when using the browser to examine the first pass.


## Usage
These instructions invoke HTLFC simply as `htlfc`.  Depending on the user's environment, it may be necessary to include the full path to the executable.

### Command Line
Try this from the command line:

>`$ htlfc infile outfile`

Where `infile` is one of the supported hypertext formats and (the optional) `outfile` will contain the result of conversion.

When `outfile` is not specified, the result would be saved to `infile.html` - unless `infile.html` represented `file+dir` format, then it's output filename would be mangled to avoid overwriting the input.

Useful command line options:
>`-h | --help` - brief usage summary.

>`-p | --pause` - examine the input after unpack.

>`-v | --version` - report latest release plus any recent commits.

### Browser
To examine the unpacked `infile` with the default browser of your operating system:

>`$ htlfc --browser infile`

>`$ htlfc -b infile` - examine result of pass 1, the unpacked files.

>`$ htlfc-b infile` - examine result of pass 2, the converted file.


Hint: rather than permanently converting your archived hypertext files, create a file association between `htlfc-b` and each of the supported file types. When opening one of these files through a file manager, HTLFC will launch your browser with the unpacked file.

### Graphical User Interface
Select your input and output files through a graphical dialogue:

>`$ htlfc --gui`

>`$ htlfc -g`

This interface offers an assisted workflow whereby HTLFC will look for all files under a specified directory.  Then, for each file found, the user may:

  * examine the unpacked pass 1 files in default browser,
  * examine pass 2 conversion also in browser,
  * convert the input and save output to new file,
  * optionally delete the input file,
  * copy the input file's timestamp to the output.

## Product

### Installation
Follow the instructions at [INSTALL](INSTALL.md)

### License
HTLFC is licensed under AGLPv3 in accordance with the file `LICENSE` in the root directory of the project.  Choice of license is explained at [AboutLicense](AboutLicense.md)

### Contributing
Developer does not expect to grow the product.  However, contributions to that end are welcome as described in [CONTRIBUTING](CONTRIBUTING.md)

