#!/usr/bin/env python3
"""Solicit input file from user and/or quit"""
import os
import tkinter as tk
from tkinter import ttk ,filedialog

def select(frame):
    """Open a dialog in <frame> to solicit filename"""

    window = frame.master  # fetch parent window
    window.filename = None # selected file

    btn1default = "Select file..."
    def button1():
        """Call to dialog 'ask open filename' """
        filename = filedialog.askopenfilename(title="Select file"
                   ,filetypes = [("legacy files",".mht .mhtml .maff .war")
                                ,("file+dir",".html")])
        if len(filename) is 0: return
        if os.path.isfile(filename):
            window.filename = filename
        window.refresh()
        return
    btn1 = tk.Button(frame ,text=btn1default ,width=60
                           ,anchor=tk.W ,command=button1)
    btn1.grid(row=1, column=2, sticky='W')

    def button2():
        """Quit button"""
        window.quit()
    btn2 = tk.Button(frame ,text="Quit"
                           ,anchor=tk.W ,command=button2)
    btn2.grid(row=1, column=3, sticky='W')

    def refresh():
        filename = window.filename
        if filename is not None:
            btn1.configure(text=filename)
        else:
            btn1.configure(text=btn1default)

    frame.refresh = refresh # for access by refresh()
