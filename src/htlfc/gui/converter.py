#!/usr/bin/env python3
"""Convert and save selected file"""
import os
import tkinter as tk
from tkinter import ttk ,messagebox

from htlfc.agents import loader
from htlfc.merger import convert

def converter(frame):
    """Open a dialog in <frame> to convert file to .html with options"""

    window = frame.master  # fetch parent window
    deletefile = tk.BooleanVar()
    keepmtime = tk.BooleanVar()
    keepmtime.set(True)

    def outfile_name(infile):
        """Generate a unique name from infile
        store the result in entOutfile
        """
        path,fullname = os.path.split(infile)
        name,ext = os.path.splitext(fullname)
        filename = os.path.join(path,f"{name}.html")
        i = 1
        while os.path.exists(filename):
             filename = os.path.join(path,f"{name}({i}).html")
             i += 1
        entOutfile.delete(0,tk.END)
        entOutfile.insert(tk.END, filename)
        return

    lb2 = ttk.Label(frame, text="Convert to:")
    lb2.grid(row=2, column=1, sticky='E', padx=5, pady=5, ipadx=5, ipady=5)
    entOutfile = ttk.Entry(frame, width=60)
    entOutfile.grid(row=2, column=2, sticky='W')

    lb3 = ttk.Label(frame, text="Then...")
    lb3.grid(row=3, column=1, sticky='E', padx=5, pady=5, ipadx=5, ipady=5)
    ckb1 = ttk.Checkbutton(frame, text="Delete original", variable=deletefile )
    ckb1.grid(row=3, column=2, sticky='W')
    ckb2 = ttk.Checkbutton(frame, text="Preserve timestamp", variable=keepmtime)
    ckb2.grid(row=4, column=2, sticky='W')

    def conversion():
        """Convert the file pointed to by window.filename
        return@success = source object
        return@failure = None
        """
        filepath = window.filename
        st = os.stat(filepath) # see below, preserve timestamp
        try:
            source = loader.unpack(filepath)
        except Exception as err:
            messagebox.showerror('Error',f"Error during unpack: {err}")
            return None
        if source is None:
            messagebox.showerror('Error',f"Unable to unpack {filepath}")
            btn2.config(state=DISABLED)
            return None
        try:
            target = convert.convert(source) # conversion
        except:
            messagebox.showerror('Error',"Conversion failed.")
            return None
        try:
            outfile = entOutfile.get()
            target.write_file(outfile)
        except:
            messagebox.showerror('Error',"Unable to write output file.")
            return None
        if keepmtime.get() is True: # preserve timestamp
            os.utime(outfile ,(st.st_atime, st.st_mtime))
        return source

    def button2():
        source = conversion()
        if source is not None:
            if deletefile.get() is True:
                source.delete()
                deletefile.set(False)
                if hasattr(source,"rename"):
                    oldname = entOutfile.get()
                    source.rename(oldname)
        window.filename = None
        window.refresh()
        return

    btn2 = ttk.Button(frame, state=tk.DISABLED
                      ,text="Convert and Save", command=button2)
    btn2.grid(row=5, column=2, sticky='W')

    def refresh():
        filename = window.filename
        if filename is None:
            entOutfile.delete(0,tk.END)
            btn2.config(state=tk.DISABLED)
        else:
            outfile_name(filename)
            btn2.config(state=tk.ACTIVE)

    frame.refresh = refresh # for access by refresh()
