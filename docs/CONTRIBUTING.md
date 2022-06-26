# Contributing

## Product Status
Hypertext Legacy File Converter "HTLFC" has satisfied the developer's needs.  Accordingly, little appetite remains to develop additional functionality beyond initial release. However, custodianship of the repository is assumed.

HTLFC is released on GitHub with the primary aim being to share it's solution with others. As a secondary objective: GitHub was chosen to enable, anyone skilled in Python, to write and submit changes.

## File Agents
It is plausible that web browser hypertext may exist in file formats complimentary to those already supported by HTLFC.  Accordingly, the repository is open to contributions of additional File Agents.  For the most part, the job of a File Agent is simply to unpack the container in temporary storage and find the `index.html` file.  However, some file formats may require adjustments (I'm looking at you MHT).

Examination of the modules in the `agents/` directory would provide a starting point for programmers wanting to unpack other file formats.  The file [Agents_API.md](../agents/Agents_API.md) should also be consulted at the outset.

## Merger
The objective of the second pass is to "in-line" various files into the main hypertext tree. Be aware of these residual risks:

>* It is possible that a style of referencing files exists, that has not been correctly converted into the in-line equivalent.

>* In-line content is base64 encoded and has passed the developer's tests using typical samples from the Web. The possibility remains that incompatible content exists.

The applicable code is at `merger/xmltree.py`.  Fault finding HTML is difficult, so to anyone who has the means to successfully trace a fault, please also submit a proven remedy.
