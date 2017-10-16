#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-09-11 at 09:59

@author: cook



Version 0.0.0
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.table import Table
from astropy import units as u
from tqdm import tqdm
import warnings
import os
import shutil

# =============================================================================
# Define variables
# =============================================================================
WORKSPACE = "/scratch/Journals/my_papers/Paper_June2017_submit/"
NEWFOLDER = WORKSPACE + 'merged/'
NEWMAIN_FILENAME = 'main.tex'
MAIN_FILE = WORKSPACE + 'paperJune2017_V1.11.tex'
# -----------------------------------------------------------------------------

# =============================================================================
# Define functions
# =============================================================================
def open_tex(filename):
    print('\n\t Opening {0}'.format(filename))
    f = open(filename, 'r')
    contents = f.readlines()
    f.close()
    return contents


def replace_input(content, filepath):
    input_str, linkstart, linkend = '\input', '{', '}'
    newcontent = []
    for line in content:
        if input_str not in line:
            newcontent.append(line)
            continue
        else:
            link = line.split(linkstart)[-1].split(linkend)[0]
            pargs = [input_str, linkstart, link, linkend]
            print('\n\t Replacing {0}{1}{2}{3} with content'.format(*pargs))
            inputcontents = open_tex('{0}/{1}'.format(filepath, link))
            for inputcontent in inputcontents:
                newcontent.append(inputcontent)
    return newcontent


def replace_figures(content, filepath, newfilepath):
    figure_str, figurestart, figureend = '\includegraphics', '{', '}'
    figure_number = 1
    newcontent = []
    for line in content:
        if figure_str not in line:
            newcontent.append(line)
            continue
        else:
            figure = line.split(figurestart)[-1].split(figureend)[0]
            pargs = [figure_str, figurestart, figure, figureend]
            print('\n\t Dealing with {0}{1}{2}{3}'.format(*pargs))
            ext = figure.split('.')[-1]
            newfigname = 'Figure{0}.{1}'.format(figure_number, ext)
            # replace in contents
            line = line.replace(figure, newfigname)
            newcontent.append(line)
            # copy old figure to new figure
            oldpath = '{0}/{1}'.format(filepath, figure)
            newpath = '{0}/{1}'.format(newfilepath, newfigname)
            print('\n\t\t Copying to {0}'.format(newfigname))
            shutil.copy(oldpath, newpath)
            # finally increase the figure number
            figure_number += 1
    return newcontent


def replace_bib(content, mainfile):
    bib_str = r'\bibliography'
    bib_file = mainfile.replace('.tex', '.bbl')
    newcontent = []
    for line in content:
        if bib_str not in line:
            newcontent.append(line)
            continue
        else:
            print('\n\t bibliography found')
            bibcontents = open_tex(bib_file)
            for bibcontent in bibcontents:
                newcontent.append(bibcontent)
    return newcontent


def save_lines_as_tex(lines, filepath, filename):
    f = open('{0}/{1}'.format(filepath, filename), 'w')
    f.writelines(lines)
    f.close()

# =============================================================================
# Start of code
# =============================================================================
# Main code here
if __name__ == "__main__":
    # ----------------------------------------------------------------------
    # open with main file
    print('\n Loading main tex file...')
    lines = open_tex(MAIN_FILE)
    main_file = MAIN_FILE.split('/')[-1]
    filepath = MAIN_FILE.split(main_file)[0]
    # need to replace all /input with content
    print('\n Dealing with inputs...')
    lines = replace_input(lines, filepath)
    # need to rename figures 1, 2, 3 etc and move to new folder
    print('\n Dealing with figures...')
    lines = replace_figures(lines, filepath, NEWFOLDER)
    # need to replace \bibliography with bbl file
    print('\n Dealing with bibliography...')
    lines = replace_bib(lines, MAIN_FILE)
    # need to save new main file to new folder
    print('\n Saving main tex file to disk...')
    save_lines_as_tex(lines, NEWFOLDER, NEWMAIN_FILENAME)



# =============================================================================
# End of code
# =============================================================================
