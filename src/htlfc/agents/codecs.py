#!/usr/bin/env python3
"""Helper function to both read and decode files"""
import re
import chardet

def get_text(filename):
    """Open filename, determine it's encoding and decode
    filename:str = path to file
    return@success (content,encoding)
        content:str = decoded content of filename
        encoding:str iff explicit (as defined in the meta tag)
                     or None
    exception:
        EOFError = file is empty
    """
    with open(filename,'rb') as infile:
        raw_str = infile.read()
    if len(raw_str) == 0:
        raise EOFError(f"File is empty: {filename}")

    # look for "charset=word" in the meta tag (word includes - and _)
    re_charset = re.compile(b'<meta.*charset=([\w\-_]+).*>' ,flags=re.IGNORECASE)
    items = re_charset.findall(raw_str)
    encoding = None
    for item in items:
        try:
            found = item.decode().lower()
            content = raw_str.decode(encoding=found)
            encoding = found
            break
        except UnicodeDecodeError:
            continue

    if encoding is None:
        # detect encoding with chardet
        try:
            found = chardet.detect(raw_str)['encoding']
            content = raw_str.decode(found)
            encoding = None
        except UnicodeDecodeError:
            raise RuntimeError(f"Unable to detect character set and decode file: {infile}")

    if content is not None:
        content = content.replace('&quot;','"')
    return (content,encoding)
