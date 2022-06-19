#!/usr/bin/env python3
""" Graphical front end """  
import tkinter as tk

from gui import select
from gui import find
from gui import viewer
from gui import converter

def interface():
    """Solicit parameters from user"""

    # Main window and notebook tabs.
    window = tk.Tk()
    window.title("Hypertext Legacy File Converter")
    window.geometry('800x400')
    window.lookatme=True

    # https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
    window.eval("tk::PlaceWindow . center") # far from perfect (better than in a corner)

    frmSelect = tk.LabelFrame(window ,relief=tk.RAISED , bd=2 ,text="Select")
    frmSelect.pack(side=tk.TOP ,fill=tk.BOTH ,expand=True)
    select.select(frmSelect)

    frmFind = tk.LabelFrame(window ,relief=tk.RAISED , bd=2 ,text="Find")
    frmFind.pack(side=tk.TOP ,fill=tk.BOTH ,expand=True)
    find.find(frmFind)

    frmBrowse = tk.LabelFrame(window ,relief=tk.RAISED , bd=2 ,text="Browser")
    frmBrowse.pack(side=tk.TOP ,fill=tk.BOTH ,expand=True)
    viewer.viewer(frmBrowse)

    frmConvert = tk.LabelFrame(window ,relief=tk.RAISED , bd=2 ,text="Convert")
    frmConvert.pack(side=tk.TOP ,fill=tk.BOTH ,expand=True)
    converter.converter(frmConvert)

    def global_refresh():
        frmSelect.refresh()
        frmFind.refresh()
        frmBrowse.refresh()
        frmConvert.refresh()
    window.global_refresh = global_refresh

    # Launch the GUI.
    window.mainloop()
    return

