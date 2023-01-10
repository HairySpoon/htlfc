#!/usr/bin/env python3
"""File agent for Mozilla Archive Format"""
import os
import tempfile
import zipfile

class maff_agent():

    def __init__(self, filename: str):
        """ Unpack maff - which is a zip file """
        self.tempdir = tempfile.TemporaryDirectory()
        tempdirpath = self.tempdir.name
        self.filename = filename

        # Validation
        try:
            zip_ref = zipfile.ZipFile(self.filename, 'r')
        except:
            raise TypeError("File apparently not zip format.")
        try:
            # extract the randomly named directory...
            root = os.path.dirname(zip_ref.namelist()[0])
        except KeyError:
            zip_ref.close()
            raise TypeError("File is missing the expected directory.")
        index = os.path.join(root,"index.html")

        # Extract
        try:
            zip_ref.extractall(tempdirpath)
        except: 
            raise TypeError("Unable to unzip file contents.")
        finally:
            zip_ref.close()

        self.basedir = os.path.join(tempdirpath,root)
        self.indexfile = os.path.join(self.basedir,'index.html')

    """
    There exist (at least) two variants of maff files:
    1. basedir/index.html with all files in basedir
    2. basedir/index.html with files in basedir/index_files, where: 
       references from index.html are prefixed by "index_files"
       references from files within index_files do not use the prefix
    """

    def walk(self):
        """ A wrapper around os.walk() """
        for dirpath, dirx, files in os.walk(self.basedir):
            yield (dirpath, dirx, files)
        return

    def delete(self):
        """Delete original file"""
        os.remove(self.filename)
        return
