#!/usr/bin/env python3
"""File agent for web archive(Konqueror)"""
import os
import tarfile
import tempfile

class war_agent():
    def __init__(self, filename: str):
        """ Unpack .war file which is a tar archive """
        self.tempdir = tempfile.TemporaryDirectory()
        self.filename = filename
        tempdirpath = self.tempdir.name
        try:
            tarball = tarfile.TarFile.gzopen(self.filename)
        except:
            raise TypeError("File apparently not tar format.")
        try:
            tarball.extractall(tempdirpath)
        except:
            raise TypeError("Unable to extract tar data.")
        finally:
            tarball.close()

        self.basedir = tempdirpath
        self.indexfile = os.path.join(self.basedir,'index.html')

    def walk(self):
        """ A wrapper around os.walk() which pre-appends the primary
        html file to the generator """
        if len(self.basedir) == 0:
            yield ('.', [], [self.indexfile])
        else:
            yield (self.basedir, [], [self.indexfile])
        for dirpath, dirx, files in os.walk(self.basedir):
            yield (dirpath, dirx, files)
        return

    def delete(self):
        """Delete original file"""
        os.remove(self.filename)
        return
