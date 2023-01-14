#!/usr/bin/env python3
"""File agent for mime hypertext "mht" "mhtml" content"""
import os
import email
import tempfile
import chardet

from htlfc.agents import codecs

class mht_agent():
    def __init__(self, filename: str):
        """ Unpack .mht file which contains MIME like email """
        self.tempdir = tempfile.TemporaryDirectory()
        self.basedir = self.tempdir.name
        self.filename = filename
        infile = open(self.filename, 'rb')
        try:
            data = email.message_from_binary_file(infile)
            if data.get_boundary() is None : raise
        except:
            raise TypeError("Unable to extract MIME data.")
        finally:
            infile.close()
        self.indexfile = '' # resolved during First Pass
        self.manifest = dict() # {"datapath":"filepath"}

        # First Pass
        counter = 1
        for part in data.walk():
            # multipart/* are just containers
            if part.get_content_maintype() == 'multipart': continue
            datapath = part.get('Content-Location')
            file_type = part.get_content_subtype()
            filename = 'part-%04d.%s' % (counter,file_type)
            counter += 1
            filepath = os.path.join(self.basedir ,filename)
            with open(filepath, 'wb') as fp:
                fp.write(part.get_payload(decode = True))
            if len(self.indexfile) == 0:
                self.indexfile = filepath # first part is always the main html
            self.manifest.update({datapath:filepath})

    def walk(self):
        """A wrapper around os.walk()"""
        for dirpath, dirx, files in os.walk(self.basedir):
            yield (dirpath, dirx, files)
        return

    def browser_fix(self):
        """Convert all external URLs into tempdir path.
        This is only used for the browser, not for actual conversion.
        """
        files = 0 ; found = 0
        for datapath,filepath in self.manifest.items() :
            path,ext = os.path.splitext(filepath)
            # Rename dubious extensions
            newname = ''
            if 'javascript' in ext:
                newname = path + '.js'
            if '+' in ext:
                a,b = ext.split('+')
                newname = path + a 
            if len(newname) > 0:
                self.manifest[datapath] = newname
                os.rename(filepath,newname)
            # Fix frames (ie html files)
            if ext in ['.htm','.html','.shtml'] :
                files +=1
                modified = self.__fix_file(filepath)
                found += int(modified)
            # Replace datapath in stylesheets
            if ext in ['.css']:
                files +=1
                modified = self.__fix_style(filepath)
                found += int(modified)
        #print(f"Fixed {found} of {files}")

    def __fix_file(self,thisfile):
        """Read, modify and write thisfile"""
        modified = False
        try:
            content,_ = codecs.get_text(thisfile)
        except EOFError as err:
            return modified
        for datapath,filepath in self.manifest.items() :
            filename = os.path.basename(filepath)
            if content.count(datapath):
                content = content.replace(datapath,filename)
                modified = True
            dp_encoded = datapath.replace('&','&amp;')
            if content.count(dp_encoded) : 
                content = content.replace(dp_encoded,filename)
                modified = True
        if modified :
            with open(thisfile,'w') as outfile:
                outfile.write(content)
        return modified

    def __fix_style(self,thisfile):
        with open(thisfile,'r') as infile:
            content = infile.read()
        modified = False
        for datapath,filepath in self.manifest.items() :
            filename = os.path.basename(filepath)
            if content.count(datapath):
                content = content.replace(datapath,filename)
                modified = True
        if modified :
            with open(thisfile,'w') as outfile:
                outfile.write(content)
        return modified
   
    def delete(self):
        """Delete original file"""
        os.remove(self.filename)
        return
