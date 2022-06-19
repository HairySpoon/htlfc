#!/usr/bin/env python3
"""Load hypertext file by calling the applicable handler"""
import os.path
import tempfile

# Handlers for each file type container
from agents.mht import mht_handler
from agents.maff import maff_handler
from agents.war import war_handler
from agents.filedir import filedir_handler
from merger import manifest

# Dictionary used by both unpack() and htlfc.__main__
mapping = {
    ".maff"    : maff_handler,
    ".mht"     : mht_handler,
    ".mhtml"   : mht_handler,
    ".war"     : war_handler,
    ".html"    : filedir_handler,
    ".shtml"   : filedir_handler }

def unpack(filename):
    """Open the archive container return a 'source' object"""

    ext = os.path.splitext(filename)[1]
    if mapping.get(ext) is None :
        print("Input file extension not understood... aborting")
        return None
    try:
        handler = mapping.get(ext, lambda: 'nothing')
        source = handler(filename)
    except TypeError as err:
        print(f"Input rejected: {err}")
        return None

    if not hasattr(source,"manifest"):
        manifest.make(source)
    return source

def dump(source):
    """Write manifest and frames to file system at tempdir.
    For debugging purposes only.
    """

    if hasattr(source, 'tempdir'):
        tempdir = source.tempdir
        print(f"Source unpacked at {tempdir.name}")
    else:
        tempdir = tempfile.TemporaryDirectory()

    manifest=os.path.join(tempdir.name,'manifest.txt')
    with open(manifest,'w') as fp:
        for datapath,filepath in source.manifest.items() :
             fp.write("%s | %s \n\n" % (datapath,filepath))

    index=os.path.join(tempdir.name,'index.txt')
    with open(index,'w') as fp:
        fp.write(f"Index File: {source.indexfile}")
    print(f"index.txt, and manifest.txt at {tempdir.name}")
    input("Continue...")
    return

