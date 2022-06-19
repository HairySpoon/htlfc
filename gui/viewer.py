#!/usr/bin/env python3
"""Launch browser with selected file"""
import os
import time
import webbrowser
import tkinter as tk
from tkinter import messagebox

from agents import loader
from merger import convert

def launch_browser(source,filename):
    """Launch webbrowser with either source or filename
    source:object - as loaded by handler agent
    filename:str - full path to index.html or equivalent
    ** Only one is required, the other must be None **
    """
    # Applicable to mht handler for browser support
    if hasattr(source,"browser_fix"):
        source.browser_fix()

    # Find index file
    if source is not None:
        indexhtml = source.indexfile
    elif filename is not None:
        indexhtml = filename
    else:
        raise RuntimeError("Nothing to browse.")

    # Redirect stderr
    newstderr = os.dup(2)
    devnull = os.open('/dev/null', os.O_WRONLY)
    os.dup2(devnull, 2)
    os.close(devnull)

    # Launch browser
    webbrowser.open(indexhtml)
    time.sleep(5)

    # Unblock stderr
    sys.stderr = os.fdopen(newstderr, 'w')
    return

def viewer(frame):
    """ Open a dialog in <frame> to launch browser
    (no actual conversion takes place) """
    window = frame.master  # fetch parent window

    def button2():
        filepath = window.filename
        source = loader.unpack(filepath)
        if source is None:
            messagebox.showerror('Error',f"Unable to unpack file {filepath}")
            btn2.config(state=tk.DISABLED)
            btn3.config(state=tk.DISABLED)
        else:
            launch_browser(source,None)
        return
    btn2 = tk.Button(frame ,text="Unpack and Open Browser" ,command=button2)
    btn2.grid(row=1 ,column=1 ,sticky=tk.W)

    def button3():
        filepath = window.filename
        source = loader.unpack(filepath)
        if source is None:
            messagebox.showerror('Error',f"Unable to unpack file {filepath}")
            btn2.config(state=tk.DISABLED)
            btn3.config(state=tk.DISABLED)
        else:
            target = convert.convert(source) # conversion
            tempfile = os.path.join(source.tempdir.name,"tempfile.html")
            with open(tempfile,'w') as fp:
                target.write_file(fp)
            launch_browser(None,tempfile)
        return
    btn3 = tk.Button(frame
                      ,text="...and Convert then Open Browser" ,command=button3)
    btn3.grid(row=1 ,column=2 ,padx=5 ,sticky=tk.W)

    def refresh():
        filename = window.filename
        if filename is not None:
            btn2.config(state=tk.ACTIVE)
            btn3.config(state=tk.ACTIVE)
        else:
            btn2.config(state=tk.DISABLED)
            btn3.config(state=tk.DISABLED)

    frame.refresh = refresh # for access by global_refresh()
    refresh()
