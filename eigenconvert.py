"""
name: eigenconvert.py
usage: eigenconvert.py <inputfile>
author: Sean Anderson (https://github.com/roguephysicist)

This is a standalone script that converts an unformatted EIG file produced by
ABINIT to a plottable file.
"""

import sys
import re

def eigenformat(inputfile, outputfile):
    """ formats ABINIT eig file for easy plotting """
    print "Reading file {0}".format(inputfile)
    with open(inputfile, "r") as ifile:
        text = ifile.read().replace('\n', '').replace('kpt#', '\n')
    sub = re.sub(r',.*\)', "", text)
    final = '\n'.join(sub.split('\n')[1:])
    with open(outputfile, "w") as ofile:
        ofile.write(final)
    print "Created formatted eigenvalue file {0}".format(outputfile)

eigenformat(sys.argv[1], 'eigen.dat')
