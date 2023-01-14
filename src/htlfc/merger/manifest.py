#!/usr/bin/env python3
"""Build source.manifest and source.frames"""  
import os
import re
import urllib.parse

from htlfc.agents import codecs

def make(source):
    """Use source.walk() to identify datapath and filepath
    populate source.manifest and source.frames
    source:object - created by file agent
    """
    source.manifest = dict() # key=datapath value=filepath

    def _pathfinder(datapath,base):
        """Search for datapath (a URL string taken from html or css)
        starting at directory base
        if a match is found:
            attach to either source.frames or source.manifest
        """
        path = urllib.parse.unquote(datapath)
        path = os.path.normpath(path) # OS specific
        for dirpath, dirx, files in os.walk(base):
          for thisfile in files:
              fullpath = os.path.join(dirpath,thisfile)
              if fullpath.endswith(path):
                  source.manifest.update({datapath:fullpath})
                  return

    # Scrape .html and .css for references to local files
    re_href = re.compile('^href="(.*?)"',flags=re.IGNORECASE)
    re_src = re.compile('^src="(.*?)"',flags=re.IGNORECASE)
    re_bkg = re.compile('^background="(.*?)"',flags=re.IGNORECASE)
    re_url = re.compile('^url[(](.*?)[)]',flags=re.IGNORECASE)
    for dirpath, dirx, files in source.walk():
        for thisfile in files:
            if thisfile.endswith(('.shtml','.html','.htm','.css')):
                try:
                    content,_ = codecs.get_text(os.path.join(dirpath,thisfile))
                except EOFError:
                    continue
                content = content.split() # now a list of strings
                items = filter(re_href.match,content)
                for item in items:
                    url = item.split('"')[1]
                    _pathfinder(url,dirpath)
                items = filter(re_src.match,content)
                for item in items:
                    url = item.split('"')[1]
                    _pathfinder(url,dirpath)
                items = filter(re_bkg.match,content)
                for item in items:
                    url = item.split('"')[1]
                    _pathfinder(url,dirpath)
                items = filter(re_url.match,content)
                for item in items:
                    url = re.split("\(|\)",item)[1]
                    if '"' in url:
                        url = item.split('"')[1]
                    _pathfinder(url,dirpath)
