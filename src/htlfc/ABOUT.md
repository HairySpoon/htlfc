## Hypertext Legacy File Converter

`htlfc` converts the following file types into a single `.html` file:

* `.maff` - Mozilla Archive File Format, as produced by the Firefox extension of the same name.
* `.mht|.mhtml` - MIME Hypertext.
* `.war` - Web ARchive as produced by the KDE Konqueror web browser.
* `file+dir` - web page having been saved as *filename*.html plus *filename_files/* (the native "Save As" format provided by Firefox and Chrome).

### Usage
`$ htlfc infile [outfile]`
&mdash; convert *infile* from the command line.

`$ htlfc --browser infile`
&mdash; unpack *infile* and open browser.

>Hint: associate extensions *.maff* *.mht* etc with `htlfc-b` so that your file manager will launch `htlfc` which in turn opens the browser.

`$ htlfc --gui`
&mdash; launch the assisted workflow.

> From a specified starting directory, workflow searches for candidate files which the user may examine and/or convert permanently to `.html`

Detailed instructions appear in the `README.md` file at the GitHub repository (NOT included in this package).
