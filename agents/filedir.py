#!/usr/bin/env python3
"""File agent for file+directory content"""
import os
import shutil

class filedir_agent():

    def __init__(self, filename: str):
        self.filename = filename
        self.indexfile = filename # required for browser()
        self.stem,self.basename = os.path.split(filename)
        files_dir = os.path.splitext(self.basename)[0]+'_files'
        self.rootpath = os.path.join(self.stem,files_dir)
        if not os.path.isdir(self.rootpath):
            raise FileNotFoundError\
            (f"Expected directory not found - '{self.rootpath}'")

    def walk(self):
        """ A wrapper around os.walk() which pre-appends the primary
        html file to the generator """
        if len(self.stem) == 0:
            yield ('.', [], [self.basename])
        else:
            yield (self.stem, [], [self.basename])
        for dirpath, dirx, files in os.walk(self.rootpath):
            yield (dirpath, dirx, files)
        return

    def delete(self):
        """Delete original file plus the _files directory"""
        os.remove(self.filename)
        shutil.rmtree(self.rootpath)
        return

    def rename(self,from_name):
        """Rename converted .html back to self.filename"""
        os.rename(from_name,self.filename)
