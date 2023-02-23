#!/usr/bin/env python3
"""File agent for file+directory content"""
import os
import shutil

class filedir_agent():

    def __init__(self, filename: str):
        self.filename = filename
        self.indexfile = filename # required for browser()
        self.stem,self.basename = os.path.split(filename)
        if len(self.stem) == 0:
            self.stem = "."
        fileroot = os.path.splitext(self.basename)[0]
        # search for a directory named like filename_word
        # where word is "files" only when language is english
        files_dir = None
        with os.scandir(self.stem) as itor:
            for entry in itor:
                if entry.is_dir() \
                and entry.name.startswith(fileroot+"_"):
                    index = entry.name.rfind("_")
                    if entry.name[:index] == fileroot \
                    and entry.name[index+1:].isalpha():
                        files_dir = entry.name
                        break
            itor.close()
        if files_dir is None:
            raise FileNotFoundError("Files directory not found.")
        else:
            self.rootpath = os.path.join(self.stem,files_dir)

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
