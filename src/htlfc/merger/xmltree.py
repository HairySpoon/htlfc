#!/usr/bin/env python3
"""Element Tree for Hyper Text Legacy File Converter"""  

import os.path
import lxml.etree
import io
import mimetypes
import base64
import html
import importlib.resources

from htlfc.agents import codecs

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
        self.forest = list() # of (filepath,etree,encoding)
        self.parser = lxml.etree.HTMLParser()
        self.__new_tree(filepath)

    def __new_tree(self,filepath):
        """Decode and parse html file. Append to self.forest
        filepath:str
        return@success etree
        """
        try:
            content,encoding = codecs.get_text(filepath)
        except EOFError as err:
            raise RuntimeError(f"File is empty: {filepath}")
        else:
            etree = lxml.etree.parse(io.StringIO(content),self.parser)
        self.forest.append((filepath,etree,encoding))
        return etree

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
                        for filepath1,_,_ in self.forest :
                            if filepath == filepath1 : continue # duplicate
                        new_etree = self.__new_tree(filepath)
                        _find_a_frame(new_etree ,depth+1) # recurse
            return

        # add frames for primary etree and recurse for every file that is added
        _,primary,_ = self.forest[0]
        _find_a_frame(primary,0)

    def add_info_bar(self,metadata):
        """Add an info bar across the top of page
        metadata:dict
            metadata['timestamp']:str
            metadata['url']:str
        """
        head = self.forest[0][1].find("head")
        if head is None: # add <head> element to root
            root = self.forest[0][1].getroot()
            head = lxml.etree.fromstring('<head/>')
            root.insert(0,head)
        with importlib.resources.open_text("merger", "infobar.css") as fp:
            info_css = lxml.etree.fromstring(fp.read())
        head.append(info_css)
        body = self.forest[0][1].find("body")
        if body is not None:
            if 'url' in metadata:
                info_text = f"[{metadata['url']}]"
            else:
                info_text = ""
            if 'timestamp' in metadata:
                info_text += f" {metadata['timestamp']}"
            info_text = html.escape(info_text) # eg symbols like "&"
            info = lxml.etree.fromstring(f'<div class="info_bar">{info_text}</div>')
            body.insert(0,info)

    def cascade(self,datapath,filepath):
        """Look for included styles and replace with in-line text
        datapath:str = path to a style object as it appears within the HTML
        filepath:str = path to a style object in local storage
        return@success = count
            count:int = how many matches were found and replaced
        """
        count = 0

        # looking for attribute href="datapath" when used with stylesheet
        attribute = './/*[@href="{}"]'.format(datapath) # XPath for an attribute
        for _,etree,_ in self.forest:
          for element in etree.findall(attribute):
              if filepath.lower().endswith('.css'):
                  element.attrib.pop('href')
                  element.tag = 'style' # may have been 'link'
                  newtext = self.__file2text(filepath)
                  element.text = newtext
                  count += 1

        # looking for tag style with text "import url()"
        pattern = '@import url("{}");'.format(datapath)
        tag = './/*style' # XPath for a tag
        for _,etree,_ in self.forest:
          for element in etree.findall(tag):
              if element.text is None : continue
              if element.text.find(pattern) > 0 :
                  newtext = self.__file2text(filepath)
                  element.text = element.text.replace(pattern,newtext)
                  count += 1

        # looking for tag <style> with text url("itemname")
        pattern = 'url("{}")'.format(datapath)
        tag='.//*style' # XPath for a tag
        for _,etree,_ in self.forest:
          for element in etree.findall(tag):
              if element.text is None : continue
              if element.text.find(pattern) > 0 :
                  newtext = 'url({})'.format(self.__file2text(filepath))
                  element.text = element.text.replace(pattern,newtext)
                  count += 1

        return count

    def substitute(self,datapath,filepath):
        """Look for included objects and replace with uri
        datapath:str = path to an object as it appears within the HTML
        filepath:str = path to an object in local storage, to be converted to text
        return@success : warnings
            warnings:list of warning, if none then empty list
                warning:str = message due to failure to convert object at filepath
        """
        warnings = list()
        patterns =     ['url({})'.format(datapath)]
        patterns.append('url("{}")'.format(datapath))

        for _,etree,_ in self.forest:
            for element in etree.iter():
                # looking for attribute src="datapath"
                src = element.attrib.get('src')
                if src == datapath:
                    # src=script becomes text of the element
                    if element.tag == 'script':
                        element.text = self.__file2uri(filepath)
                        del element.attrib['src']
                    elif element.tag == 'iframe':
                        continue # defer until merge_iframes()
                    else:
                        element.attrib['src'] = self.__file2uri(filepath)

                # looking for attribute background="datapath"
                src = element.attrib.get('background')
                if src == datapath:
                    newtext = self.__file2uri(filepath)
                    element.attrib['background'] = newtext

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

        return warnings

    def __file2uri(self,filepath):
        """Helper function to convert a file at filepath
        into its text representation
        Exceptions are converted to RuntimeWarning
        """
        if os.path.getsize(filepath) == 0:
            raise RuntimeWarning(f"File is empty: {filepath}")
        uri = ['data:']
        mimetype,_ = mimetypes.guess_type(filepath, strict = False)
        # when the extension is missing, mimetypes will fail
        if mimetype is None: mimetype = 'application/octet-stream'
        uri.append(mimetype)
        uri.append(";base64,")
        try:
            with open(filepath,'rb') as fp:
                data = fp.read()
                encoded = base64.b64encode(data)
        except Exception as err:
            raise RuntimeWarning(f"b64encode error {err} | from: {filepath}")
        else:
            uri.append(encoded.decode("utf-8"))
        return ''.join(uri)

    def __file2text(self,filepath):
        """Helper function to convert any document
        at filepath into text
        Exceptions are converted to RuntimeWarning
        """
        if os.path.getsize(filepath) == 0:
            filename = os.path.basename(filepath)
            raise RuntimeWarning(f"File is empty: {filename}")
        text,_ = codecs.get_text(filepath)
        return text

    def merge_iframes(self):
        """Reduce all etrees to one"""
        _,tree,encoding = self.forest[0] # primary etree
        tag = './/*iframe' # XPath for a tag

        # Looking for level 1 iframes...
        for element1 in tree.findall(tag):
            datapath1 = element1.get('src')
            if datapath1 is None: continue
            if datapath1 in self.frames:
                target1 = self.frames[datapath1]
            else: continue
            # ignore [0] because it is the primary etree...
            for filepath1,etree1,encoding1 in self.forest[1:]:
                if filepath1 == target1:

                    # Looking for level 2 iframes...
                    for element2 in etree1.findall(tag):
                        datapath2 = element2.get('src')
                        if datapath2 is None: continue
                        if datapath2 in self.frames:
                            target2 = self.frames[datapath2]
                        else: continue
                        for filepath2,etree2,encoding2 in self.forest[1:]:
                            if filepath2 == target2:

                                # Looking for level 3 iframes...
                                for element3 in etree2.findall(tag):
                                    datapath3= element3.get('src')
                                    if datapath3 is None: continue
                                    if datapath3 in self.frames:
                                        target3 = self.frames[datapath3]
                                    else: continue
                                    for filepath3,etree3,encoding3 in self.forest[1:]:
                                        if filepath3 == target3:
                                            raise RuntimeError("Level three iframe was found but is not supported")
                                # Found level 2 iframe...
                                if encoding2 is None:
                                    frame_text2 = lxml.etree.tostring(etree2
                                                  ,method = 'html')
                                    frame_text2 = frame_text2.decode()
                                else:
                                    frame_text2 = lxml.etree.tostring(etree2
                                                  ,encoding = encoding2
                                                  ,method = 'html')
                                    frame_text2 = frame_text2.decode(encoding2)
                                # Merge into tree
                                # replace src="..path.."
                                # with    srcdoc='..inline..' (single quotes)
                                del element2.attrib['src']
                                element2.set('srcdoc',frame_text2)

                    # Found level 1 iframe...
                    if encoding1 is None:
                        frame_text1 = lxml.etree.tostring(etree1
                                      ,method = 'html')
                        frame_text1 = frame_text1.decode()
                    else:
                        frame_text1 = lxml.etree.tostring(etree1
                                      ,encoding = encoding1
                                      ,method = 'html')
                        frame_text1 = frame_text1.decode(encoding1)
                    # Merge into tree
                    # replace src="..path.."
                    # with srcdoc="..inline.." (double quotes)
                    del element1.attrib['src']
                    element1.set('srcdoc',frame_text1)

    def write_file(self,filepath):
        """Serialize the Etree
        filepath:str = path to output file
        """
        _,etree,encoding = self.forest[0]
        kwargs = { 'method':'html' } # args for tostring()
        if encoding is not None:
            kwargs['encoding'] = encoding
        result = lxml.etree.tostring(etree,**kwargs)
        with open(filepath,'wb') as fp:
            fp.write(result)

