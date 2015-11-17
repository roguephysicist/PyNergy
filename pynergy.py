"""
name: pynergy.py
author: Sean Anderson (https://github.com/roguephysicist)

This script calculates transition energies between energy bands using eigen-
energy files generated by ABINIT during a band structure calculation. This
script allows you to input a desired energy value and finds all the upward
transitions that can produce that value within a specified tolerance.

If the input file is an unformatted EIG file produced by ABINIT, you can use
the adjoining 'eigenconvert.py' program that will automatically format it to a
plottable file. You can then use that file to calculate the transitions.
"""

import sys
import numpy as np

INPUTFILE = sys.argv[1]
VALENCE = sys.argv[2]
ENERGY = sys.argv[3]
DELTA = sys.argv[4]

OFFSET = 0

def transitions(inputfile, valence, energy, delta):
    """
    loops over all values in input file and calculates upward transitions
    and selects only the ones that match the desired value.
    """
    textfile = 'transitions.dat'
    arrowfile = 'gnuplotarrows.txt'
    file1 = open(textfile, 'w') # opens output file for writing
    file2 = open(arrowfile, 'w')    # opens output file for writing
    eigen = np.loadtxt(inputfile)   # creates a numpy array from input file

    print 'Calculating transitions for {0} around {1} eV with a delta '\
          'of {2}'.format(inputfile, energy, delta)

    kpts = len(eigen)   # max k-points = file length
    bands = len(eigen[0])   # max bands = columns

    for kpt in range(0, kpts):  # loops over k-points
        for start in range(1, valence+1):   # over all valence bands
            for finish in range(valence+2, bands):  # over conduction bands
                orig = eigen[kpt, start]    # value at origin band
                targ = eigen[kpt, finish]   # value at target band
                diff = abs(orig - targ) # the difference
                # tests to see if diff is between desired value +/- delta
                if energy - delta <= diff <= energy + delta:
                    text = '{0:0>9.6f} eV | k-point: {1:0>3d} | '\
                           'bands: {2:0>2d} -> {3:0>2d}\n'\
                           .format(diff, kpt + 1, start, finish)
                    file1.write(text)
                    arrows = 'set arrow from {0},{1:.5f} to {0},{2:.5f}\n'\
                             .format(kpt + 1, orig - OFFSET, targ - OFFSET)
                    file2.write(arrows)
    file1.close()   # closes file
    print 'Writing ===> {0}'.format(textfile)
    file2.close()   # closes file
    print 'Writing ===> {0}'.format(arrowfile)

transitions(INPUTFILE, VALENCE, ENERGY, DELTA)
