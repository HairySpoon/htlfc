#!/usr/bin/env python3
"""Find candidate files under a given directory"""
import os
import tkinter as tk
from tkinter import ttk ,filedialog

from htlfc.agents import loader # search() uses "mapping"

def find(frame):
    """Open a dialog in <frame> to solicit filename"""

    window = frame.master    # fetch parent window
    frame.dirname = None     # selected directory
    frame.fileslist = list() # found legacy files

    btn1default = "All files under..."
    def button1():
        dirname = filedialog.askdirectory(title="Select Directory"
                  ,mustexist=True)
        if len(dirname) is 0: return
        if os.path.isdir(dirname):
            frame.dirname = dirname
        search()
        window.refresh()
        return
    btn1 = tk.Button(frame ,text=btn1default ,width=60
                           ,anchor=tk.W ,command=button1)
    btn1.grid(row=1, column=1, sticky=tk.W)

    def search():
        """Walk frame.dirname, find legacy html files, save results"""
        if frame.dirname is None: return
        for dirpath, dirx, files in os.walk(frame.dirname):
            if dirpath.endswith("_files"):
                dirx[:] = [] # ignores sub-dirs
                continue
            for filename in files:
                basename,ext = os.path.splitext(filename)
                ext = ext.lower()
                if ext in loader.mapping.keys():
                    if ext == ".html":
                        subdir = os.path.join(dirpath,basename)+"_files"
                        if not os.path.isdir(subdir):
                            continue
                    filepath = os.path.join(dirpath,filename)
                    frame.fileslist.append(filepath)

    def button2():
        if len(frame.fileslist) == 0:
            frame.dirname = None
            window.filename = None
        else:
            filename = frame.fileslist.pop(0)
            window.filename = filename
        window.refresh()
        return
    btn2 = tk.Button(frame ,text="Next" ,command=button2)
    btn2.grid(row=1, column=2, sticky=tk.W)

    def refresh():
        dirname = frame.dirname
        if dirname is None:
            btn1.configure(text=btn1default)
            btn2.config(state=tk.DISABLED)
        else:
            btn1.configure(text=dirname)
            btn2.config(state=tk.ACTIVE)

    frame.refresh = refresh # for access by refresh()
    refresh()
