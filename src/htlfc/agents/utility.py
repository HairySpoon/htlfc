#!/usr/bin/env python3
"""Helper function for reading files"""
import os
import chardet

def get_html(filename,hint=None):
    """Open filename, determine it's encoding and decode
    filename:str = path to file
    hint:str = prior encoding, such as from parent file index.html
    return@success (content,encoding)
        content:str = decoded content of filename
        encoding:str = detected character set
    return@failure (None,None) = empty file
    """
    print("OnD_new...")
    with open(filename,'rb') as infile:
        raw_str = infile.read()
    if len(raw_str) == 0:
        return (None,None)
    encoding = chardet.detect(raw_str)['encoding']
    content = raw_str.decode(encoding).replace('&quot;','"')
    return (content,encoding)
