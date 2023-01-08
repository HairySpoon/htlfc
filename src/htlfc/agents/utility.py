#!/usr/bin/env python3
"""Helper function for reading files"""
import os
import re
import chardet

def get_html(filename):
    """Open filename, determine it's encoding and decode
    filename:str = path to file
    return@success (content,encoding)
        content:str = decoded content of filename
        encoding:str = detected character set
    return@failure (None,None) = empty file
    """
    with open(filename,'rb') as infile:
        raw_str = infile.read()
    if len(raw_str) == 0:
        return (None,None)

    # look for "charset=word" in the meta tag (word includes - and _)
    re_charset = re.compile(b'<meta.*charset=([\w\-_]+).*>' ,flags=re.IGNORECASE)
    items = re_charset.findall(raw_str)
    encoding = None
    for item in items:
        try:
            found = item.decode().lower()
            content = raw_str.decode(found)
            encoding = found
            break
        except UnicodeDecodeError:
            continue

    if encoding is None:
        # detect encoding with chardet
        try:
            encoding = chardet.detect(raw_str)['encoding']
            content = raw_str.decode(encoding)
        except UnicodeDecodeError:
            content=None ; encoding = None

    if content is not None:
        content = content.replace('&quot;','"')
    return (content,encoding)
