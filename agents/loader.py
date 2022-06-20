#!/usr/bin/env python3
"""Load hypertext file by calling the applicable file agent"""
import os.path
import tempfile

# Agents for each file type container
from agents.mht import mht_agent
from agents.maff import maff_agent
from agents.war import war_agent
from agents.filedir import filedir_agent
from merger import manifest

# Dictionary used by both unpack() and htlfc.__main__
mapping = {
    ".maff"    : maff_agent,
    ".mht"     : mht_agent,
    ".mhtml"   : mht_agent,
    ".war"     : war_agent,
    ".html"    : filedir_agent,
    ".shtml"   : filedir_agent }

def unpack(filename):
    """Open the archive container return a 'source' object"""

    ext = os.path.splitext(filename)[1]
    if mapping.get(ext) is None :
        print("Input file extension not understood... aborting")
        return None
    try:
        agent = mapping.get(ext, lambda: 'nothing')
        source = agent(filename)
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

