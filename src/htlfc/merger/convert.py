#!/usr/bin/env python3
"""Bridge between file agents and the HTML Element Tree"""

import os

from htlfc.merger.xmltree import ET

def convert(source):
    """Convert source into xml element tree and supervise conversion
    source = file agent object
    return@success = (content,warnings)
        content:etree = based on source
        warnings = list of warning:str
    """
    warnings = list() # errors (if any) from cascade() and substitute()

    # Create Element Tree object
    indexhtml = source.indexfile
    content = ET(indexhtml)

    # Detect iframes
    content.find_iframes(source.manifest)

    # Add meta data if it exists
    if hasattr(source,"metadata") and len(source.metadata) > 0:
        content.add_info_bar(source.metadata)

    # Keep adding frames and CSS until cascade no longer finds anything
    modified = True
    while modified:
        count = 0
        for datapath,filepath in source.manifest.items() :
            extension = os.path.splitext(filepath)[1].lower()
            if extension in ['.css','.htm','.html','.shtml']:
                try:
                    count += content.cascade(datapath,filepath)
                except RuntimeWarning as err:
                    warnings.append(err)
        modified = count>0 # eventually count=0, then exit loop

    # Add everything else except CSS and iframes
    for datapath,filepath in source.manifest.items() :
        if filepath == indexhtml:
            continue # ignore top level html
        if filepath.lower().endswith('.css'):
            continue
        try:
            content.substitute(datapath,filepath) # which ignores iframes
        except RuntimeWarning as err:
            warnings.append(err)

    # Wrap iframes into the primary etree
    content.merge_iframes()

    return (content,warnings)

