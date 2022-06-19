#!/usr/bin/env python3
"""Element Tree for Hyper Text Legacy File Converter"""  

import os.path
import lxml.etree
import chardet
import io
import mimetypes
import base64

class ET():
    """Upon init, convert the primary HTML into an element tree (ET)
    and append to self.forest[]
    Subsequent calls are required as follows...
        find_iframes()  append self.forest[]
        cascade()       merge styles CSS inline - repeat until all done
        substitute()    merge external files into the ET
        merge_iframes() merge external iframes into the ET
    Finally...
        write_file()    write the ET back to a file
    """
    def __init__(self, filepath):
        self.forest = list() # of (filepath,etree)
        with open(filepath,'rb') as infile:
            instr = infile.read()
        instr_enc = chardet.detect(instr)
        self.encoding = instr_enc['encoding']
        instr = instr.decode(self.encoding)
        self.parser = lxml.etree.HTMLParser()
        etree = lxml.etree.parse(io.StringIO(instr),self.parser)
        self.forest.append((filepath,etree))

    def find_iframes(self,manifest):
        """Search for frames in manifest
        store found frames in self.frames and self.forest
        """
        # search for frames
        self.frames = dict()
        for datapath,filepath in manifest.items() :
            extension = os.path.splitext(filepath)[1].lower()
            if extension in ['.htm','.html','.shtml'] :
                self.frames.update({datapath:filepath})
                #print(f"found iframe: filepath={filepath}")
                #print(f"            : datapath={datapath[:60]}")

        def _find_a_frame(etree,depth):
            """Search for frames at this level, if found:
            - append to self.forest
            - invoke itself against the found frame
            """
            tag = './/*iframe' # XPath for a tag
            for element in etree.findall(tag):
                path = element.get('src')
                if path is None: continue
                for datapath,filepath in self.frames.items():
                    if path == datapath:
                        for filepath1,_ in self.forest :
                            if filepath == filepath1 : continue # duplicate
                        with open(filepath,'rb') as infile:
                            instr = infile.read()
                        instr = instr.decode(self.encoding)
                        instr = instr.replace('&quot;','"')
                        new_etree = lxml.etree.parse(io.StringIO(instr),self.parser)
                        self.forest.append((filepath,new_etree))
                        _find_a_frame(new_etree ,depth+1) # recurse
            return

        # add frames for primary etree and recurse for every file that is added
        _,primary = self.forest[0]
        _find_a_frame(primary,0)

    def cascade(self,datapath,filepath):
        """Look for included styles and replace with in-line text"""
        count = 0

        # looking for attribute href="datapath"
        attribute = './/*[@href="{}"]'.format(datapath) # XPath for an attribute
        for _,etree in self.forest:
          for element in etree.findall(attribute):
              element.clear()
              element.tag = 'style'
              element.text = self.__file2text(filepath)
              count += 1

        # looking for tag style with text "import url()"
        pattern = '@import url("{}");'.format(datapath)
        tag = './/*style' # XPath for a tag
        for _,etree in self.forest:
          for element in etree.findall(tag):
              if element.text is None : continue
              if element.text.find(pattern) > 0 :
                  newtext = self.__file2text(filepath)
                  element.text = element.text.replace(pattern,newtext)
                  count += 1

        # looking for url("itemname") in tag <style>
        pattern = 'url("{}")'.format(datapath)
        tag='.//*style' # XPath for a tag
        for _,etree in self.forest:
          for element in etree.findall(tag):
              if element.text is None : continue
              if element.text.find(pattern) > 0 :
                  newtext = 'url({})'.format(self.__file2text(filepath))
                  element.text = element.text.replace(pattern,newtext)
                  count += 1

        return count

    def substitute(self,datapath,filepath):
        """Search for item at datapath and
        replace with uri created from the file at filepath
        """
        patterns =     ['url({})'.format(datapath)]
        patterns.append('url("{}")'.format(datapath))

        for _,etree in self.forest:
            for element in etree.iter():
                # looking for attribute src="datapath"
                src = element.attrib.get('src')
                if src == datapath:
                    # src=script becomes text of the element
                    if element.tag == 'script' :
                        element.text = self.__file2uri(filepath)
                        del element.attrib['src']
                    elif element.tag == 'iframe':
                        continue # defer until merge_iframes()
                    else:
                        element.attrib['src'] = self.__file2uri(filepath)

                # looking for url(datapath) in the attribute style
                if element.attrib.get('style'):
                    for pattern in patterns:
                        if pattern in element.attrib["style"]:
                            newtext = 'url({})'.format(self.__file2uri(filepath))
                            element.attrib["style"] = element.attrib["style"].replace(pattern,newtext)
      
                # looking for url("datapath") in any text
                if element.text is None : continue
                for pattern in patterns:
                    if element.text.find(pattern) > 0 :
                        newtext = 'url({})'.format(self.__file2uri(filepath))
                        element.text = element.text.replace(pattern,newtext)

    def __file2uri(self,filepath):
       """Helper function to convert a file at filepath
       into its text representation
       """
       uri = ['data:']
       mimetype,_ = mimetypes.guess_type(filepath, strict = False)
       # when the extension is missing, mimetypes will fail
       if mimetype is None: mimetype = 'application/octet-stream'
       uri.append(mimetype)
       uri.append(";base64,")
       fp = open(filepath,'rb')
       data = fp.read()
       encoded = base64.b64encode(data)
       uri.append(encoded.decode(self.encoding))
       return ''.join(uri)

    def __file2text(self,filepath):
        """Helper function to convert any document
        at filepath into text
        """
        fp = open(filepath, encoding = self.encoding, mode = 'r')
        text = fp.read()
        return text

    def merge_iframes(self):
        """Reduce all etrees to one"""
        _,tree = self.forest[0] # primary etree
        tag = './/*iframe' # XPath for a tag

        # Looking for level 1 iframes...
        for element1 in tree.findall(tag):
            datapath1 = element1.get('src')
            target1 = self.frames[datapath1]
            for filepath1,etree1 in self.forest[1:]: # exclude [0] which is primary etree
                if filepath1 == target1:

                    # Looking for level 2 iframes...
                    for element2 in etree1.findall(tag):
                        datapath2 = element2.get('src')
                        target2 = self.frames[datapath2]
                        for filepath2,etree2 in self.forest[1:]:
                            if filepath2 == target2:

                                # Looking for level 3 iframes...
                                for element3 in etree2.findall(tag):
                                    datapath3= element3.get('src')
                                    target3 = self.frames[datapath3]
                                    for filepath3,etree3 in self.forest[1:]:
                                        if filepath3 == target3:
                                            print("Level three iframe was found but is not supported")

                                # Found level 2 iframe...
                                frame_text2 = lxml.etree.tostring(etree2,
                                                        encoding = self.encoding,
                                                        method = 'html')
                                frame_text2 = frame_text2.decode(self.encoding)
                                # Merge into tree - replace src="..path.." with srcdoc='..inline..' (single quotes)
                                del element2.attrib['src']
                                element2.set('srcdoc',frame_text2)

                    # Found level 1 iframe...
                    frame_text1 = lxml.etree.tostring(etree1,
                                            encoding = self.encoding,
                                            method = 'html')
                    frame_text1 = frame_text1.decode(self.encoding)
                    # Merge into tree - replace src="..path.." with srcdoc="..inline.." (double quotes)
                    del element1.attrib['src']
                    element1.set('srcdoc',frame_text1)

    def write_file(self,fp):
        """Serialize the Etree
        fp = file object
        """
        _,etree = self.forest[0]
        result = lxml.etree.tostring(etree,
                                     encoding = self.encoding, 
                                     method = 'html')
        result = result.decode(self.encoding)
        fp.write(result)

