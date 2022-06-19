# Hypertext Legacy File Converter
---
HTLFC is a Python3 utility that converts the following file types into a single `.html` file:

* `.maff` - Mozilla Archive File Format, as produced by the Firefox extension of the same name.
* `.mht` - MIME Hypertext.
* `.war` - Web ARchive as produced by the KDE Konqueror web browser (other sources of `.war` files have not been tested).
* `file+dir` - web page saved as *filename*.html plus *filename_files/* directory (the native "Save As" format used by Firefox and Chrome).

## Use Cases

The original use case for HTLFC emerged when Mozilla discontinued their legacy API; a necessity for the Firefox MAFF extension which thus became obsolete. Some users were left with collection of `.maff` and `.mht` files which could no longer be opened in the absence of that extension.

Obviously HTLFC may also be used to open and/or convert hypertext files from other sources.

## Principle of Operation
HTLFC executes two major steps:

* The input file is first unpacked into a temporary directory.  Some adjustment may take place depending on the format.
* Associated files (style sheets, images, javascript, etc) are converted into in-line format and merged into the main file.

The user may examine the unpacked content between the two steps.  Use either `-p` option "pause" from the command line, or select "Unpack and  Open Browser" from the graphical interface.

## Usage
`htlfc infile outfile`



