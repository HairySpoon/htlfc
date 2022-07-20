#!/usr/bin/env python3
"""Bridge between file agents and the HTML Element Tree"""

import os

from htlfc.merger.xmltree import ET

def convert(source):
    """Convert source into xml element tree and supervise conversion
    source = file agent object
    """
    # Create Element Tree object
    indexhtml = source.indexfile
    content = ET(indexhtml)

    # Detect iframes
    content.find_iframes(source.manifest)

    # Keep adding frames and CSS until cascade no longer finds anything
    modified = True
    while modified:
        count = 0
        for datapath,filepath in source.manifest.items() :
            extension = os.path.splitext(filepath)[1].lower()
            if extension in ['.css','.htm','.html','.shtml']:
                count += content.cascade(datapath,filepath)
        modified = count>0 # eventually count=0, then exit loop

    # Add everything else except CSS and iframes
    for datapath,filepath in source.manifest.items() :
        if filepath == indexhtml:
            continue # ignore top level html
        if filepath.lower().endswith('.css'):
            continue
        content.substitute(datapath,filepath) # which ignores iframes

    # Wrap iframes into the primary etree
    content.merge_iframes()

    return content

