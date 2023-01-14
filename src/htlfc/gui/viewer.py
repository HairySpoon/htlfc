#!/usr/bin/env python3
"""Launch browser with selected file"""
import os
import time
import tempfile
import webbrowser
import tkinter as tk
from tkinter import messagebox

from htlfc.agents import loader
from htlfc.merger import convert

def launch_browser(source,filename):
    """Launch webbrowser with either source or filename
    source:object - as loaded by file agent
    filename:str - full path to index.html or equivalent
    ** Only one is required, the other must be None **
    """
    # Applicable to mht agent for browser support
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
    """Open a dialog in <frame> to launch browser
    (no actual conversion takes place)"""
    window = frame.master  # fetch parent window

    def button2():
        filepath = window.filename
        try:
            source = loader.unpack(filepath)
        except Exception as err:
            messagebox.showerror('Error',f"Error during unpack: {err}")
            reset()
            return
        if source is None:
            messagebox.showerror('Error',f"Unable to unpack file {filepath}")
            reset()
        else:
            launch_browser(source,None)
        return
    btn2 = tk.Button(frame ,text="Unpack and Open Browser" ,command=button2)
    btn2.grid(row=1 ,column=1 ,sticky=tk.W)

    def button3():
        filepath = window.filename
        try:
            source = loader.unpack(filepath)
        except Exception as err:
            messagebox.showerror('Error',f"Error during unpack: {err}")
            reset()
            return
        if source is None:
            messagebox.showerror('Error',f"Unable to unpack file {filepath}")
            reset()
        else:
            try:
                target = convert.convert(source) # conversion
            except RuntimeError as err:
                messagebox.showerror('Error',f"Error during conversion {err}")
                return
            tempname = tempfile.NamedTemporaryFile().name
            target.write_file(tempname)
            launch_browser(None,tempname)
        return
    btn3 = tk.Button(frame
                      ,text="...and Convert then Open Browser" ,command=button3)
    btn3.grid(row=1 ,column=2 ,padx=5 ,sticky=tk.W)

    def reset():
        """Force state as if no file selected"""
        window.filename = None
        window.refresh()
        return

    def refresh():
        """Set or disable state of buttons"""
        filename = window.filename
        if filename is not None:
            btn2.config(state=tk.ACTIVE)
            btn3.config(state=tk.ACTIVE)
        else:
            btn2.config(state=tk.DISABLED)
            btn3.config(state=tk.DISABLED)
        return

    frame.refresh = refresh # for access by refresh()
    refresh() # upon init
