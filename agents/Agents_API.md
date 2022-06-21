# File Agents API

File agents prepare content for conversion by the merger tools; a consistent interface between the two systems is essential.

Responsibilities of the file agents are:

* Unpack the content into a temporary location on the file system.
* Provide the merge tools with:
    * index file - the primary HTML.
    * manifest (optional) - a dictionary, it's keys describing strings embedded in the HTML and its values being pointers to the content, the files, in the temporary location. If manifest is not provided then merger/manifest.py will be called to create it retrospectively.
* Upon exit, delete the temporary files.

Merge tools use this as follows:

* Index file is converted into an XML element tree.
* Objects described by the file map are merged into the tree.
* Resulting HTML file is written from the tree.

## Methods
Each file agent must provide the following methods:

* `self.walk()` essentially a wrapper around `os.walk()` but with the addition of any files that reside outside the tree.
* `self.delete()` to delete the original file.  Plus, for file+dir agent, to also delete the `_files` directory.

Where applicable, a file agent may also provide the following:

* `self.browser_fix()` called after unpack if a browser will be launched.
* `self.rename(old_name)` called by gui/converter.py only when original is deleted after conversion *and* the new filename had been mangled.

## Properties

These properties are attached to the objects created by the file agents.
As indicated, not all are created by the agents themselves.

### self.tempdir

When the input file is unpacked, agents will use a temporary holding area on the file system.  Temporary file deletion is assured when exit is called against
 `tempfile.TemporaryDirectory()`.

The Filedir agent does not generate `self.tempdir` because its input is structured around an existing directory.

### self.indexfile

A string pointing to a file in the temporary storage which contains HTML for the web page.  In practice, iframes in the content may introduce additional HTML files, they are represented in self.frames.

### self.frames

A dictionary of {datapath, filepath} describing every iframe.  See also self.manifest for objects other than frames.
Not created by agents, refer merger/xmltree/find_iframes(). 

### self.manifest

A dictionary of {datapath, filepath} describing every object (except frames) in the content.
Each key contains a string to be found in the HTML and replaced with the file represented by the dictionary's value.

It is a responsibility of the file agent to ensure that the keys will appear in the HTML.

>### MHT Agent
MHT files do not use sensible filenames. Instead, the original URL appears in the HTML and is used as the name of the corresponding MIME.  Within the HTML, the URL is represented as an encoded string but of necessity, the HTML will be decoded by the merge tools.  Consequently the manifest key will no longer match the resulting text.  The MHT agent solves this by rewriting the HTML with a mangled string that will match its key (also mangled to match).

>### MAFF Agent
There are two known MAFF variants.  One contains its files at the same level as the index file.  The other employs a directory "index_files" for this purpose.  The agent adjusts manifest to suit.

## Exceptions

Each agent performs validation on the input file and returns `TypeError` if the contents are not understood.

