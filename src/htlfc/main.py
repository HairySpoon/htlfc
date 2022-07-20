#!/usr/bin/env python3
""" HyperText Legacy File Converter
Parse arguments and launch the converter"""
import os.path
import sys
import argparse

# application modules
from htlfc.agents import loader
from htlfc.merger import convert
from htlfc.gui import viewer
from htlfc.gui import interface

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pause' ,action='store_true'
                       ,help = 'Pause after unpack, to examine tempdir.')
    parser.add_argument('infile' ,nargs='?'
                       ,help = "Input file: maff, mht, war, file+directory.")
    parser.add_argument('outfile' ,nargs='?'
                       ,help = "If not given, then infile with extension 'html'.")

    browser = parser.add_argument_group(
              "Convert and open in browser (requires infile)")
    browser.add_argument('-b' ,'--browser' ,action='store_true')

    graphic  = parser.add_argument_group(
              "Open a graphical interface for parameters")
    graphic.add_argument('-g' ,'--gui' ,action='store_true')

    args = parser.parse_args()

    # Validate Arguments
    abort = False
    if args.gui and args.browser:
        print("Invalid: both --gui and --browser")
        abort = True
        mode = None
    else:
        if args.browser:
            mode = 'browser'
        elif args.gui:
            mode = 'gui'
        else:
            mode = 'file'

    if (mode == 'file') or (mode =='browser'):
        if args.infile is None:
            print("Expecting input filename, not provided")
            abort = True
        else:
            infile = args.infile
            root,ext = os.path.splitext(infile)

    if mode == 'gui' or mode == 'browser':
        if args.outfile:
            print("Cannot use --output with --browser or --gui")
            abort = True

    if args.infile:
        if not os.path.isfile(args.infile):
            print("Input filename not found.")
            abort = True
        elif not os.access(args.infile,os.R_OK):
            print("Input file cannot be read.")
            abort = True

    if mode == 'file' and args.infile is not None:
        if args.outfile:
            outfile = args.outfile
        else:
            if loader.mapping.get(ext) \
            is loader.mapping.get('.html'): # detects .html & .shtml
                # mangle infile by appending underscore to root
                outfile = root + "_" + ext
            else:
                outfile = root +'.html'

    if abort:
        sys.exit(1)

    if mode == 'gui':
        interface.interface()
        sys.exit()
        
    # Load File
    if mode == 'file' or mode == 'browser':
        source = loader.unpack(infile)
        if source is None:
            sys.exit(1)

    # Browser
    if mode == 'browser':
        viewer.launch_browser(source,infile)

    # Examine tempdir
    if args.pause :
        loader.dump(source)

    # Output
    if mode == 'file':
        target = convert.convert(source) # conversion
        try:
            fp = open(outfile,'w')
        except:
            print(f"File {outfile} cannot be opened for writing")
            sys.exit(1)
        else:
            target.write_file(fp)
            fp.close()
        del target

    # Cleanup (force temp directory delete)
    del source

if __name__ == '__main__':
    main()

