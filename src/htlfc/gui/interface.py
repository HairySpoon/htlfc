#!/usr/bin/env python3
""" Graphical front end """  
import tkinter as tk

from htlfc.gui import select
from htlfc.gui import find
from htlfc.gui import viewer
from htlfc.gui import converter

def interface():
    """Solicit parameters from user"""

    # Main window and notebook tabs.
    window = tk.Tk()
    window.title("Hypertext Legacy File Converter")
    window.geometry('800x400')

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

    def refresh():
        frmSelect.refresh()
        frmFind.refresh()
        frmBrowse.refresh()
        frmConvert.refresh()
    window.refresh = refresh

    # Launch the GUI.
    window.mainloop()
    return

