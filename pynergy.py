#!/opt/science/anaconda3/bin/python
"""
name: pynergy.py
usage: pynergy.py [-h] -i INPUT -v VALENCE -e ENERGY [-d DELTA]
author: Sean Anderson (https://github.com/roguephysicist)

This script calculates transition energies between energy bands using eigen-
energy files generated by ABINIT during a band structure calculation. This
script allows you to input a desired energy value and finds all the upward
transitions that can produce that value within a specified tolerance.

If the input file is an unformatted EIG file produced by ABINIT, you can use
the adjoining 'eigenconvert.py' program that will automatically format it to a
plottable file. You can then use that file to calculate the transitions.
"""

import argparse
import numpy as np

# parses command line options
PARSER = argparse.ArgumentParser(description='This script calculates '\
                        'transition energies between energy bands '\
                        'using eigen-energy files generated by ABINIT '\
                        'during a band structure calculation. This script '\
                        'allows you to input a desired energy value and '\
                        'finds all the upward transitions that can produce '\
                        'that value within a specified tolerance.')
PARSER.add_argument('-i', '--input', help='Input file name', required=True)
PARSER.add_argument('-v', '--valence', help='Number of valence bands',
                    type=int, required=True)
PARSER.add_argument('-e', '--energy', help='Energy value in eV',
                    type=float, required=True)
PARSER.add_argument('-f', '--efermi',
                    help='Fermi energy in eV, for metals/semi-metals (optional)',
                    type=float, required=False)
PARSER.add_argument('-d', '--delta',
                    help='Energy delta in eV (default = 0.001 eV)',
                    type=float, default=0.001, required=False)
PARSER.add_argument('-o', '--offset',
                    help='Offest energy in eV, usually the VBM (optional)',
                    type=float, default=0.0, required=False)
PARSER.add_argument('-a', '--append',
                    help='Append a string to the end of the \'set arrow\' commands,'\
                          ' typically line style specifiers (optional)',
                    type=str, default='', required=False)
ARGS = PARSER.parse_args()


def gentrans(eigen, valence, energy, delta, efermi, offset, append):
    """
    loops over all values in input file and calculates upward transitions
    and selects only the ones that match the desired value.
    """
    if efermi is None:                      # sets efermi to max valence band
        VBM = np.max(eigen[:, valence])  # value, if not set by user
        CBM = np.min(eigen[:, int(valence + 1)])  # value, if not set by user
        efermi = (VBM + 0.5*(CBM - VBM)) - offset

    kpts = len(eigen)       # max k-points = file length
    bands = len(eigen[0])   # max bands = columns
    header = '# Transitions around {0: 012.8f} eV +/- {1: 012.8f} eV,\n'\
             '# efermi (w/offset) = {2: 012.8f}, plot offset = {3: 012.8f}\n'\
             .format(energy, delta, efermi, offset)

    text = [header]
    for kpt in range(0, kpts):              # loops over k-points
        for start in range(1, valence+1):   # over all valence bands
            for finish in range(valence+1, bands):  # over conduction bands
                orig = eigen[kpt, start]    # value at origin band
                targ = eigen[kpt, finish]   # value at target band
                diff = abs(orig - targ)     # the difference
                # tests to see if diff is between desired value +/- delta
                if energy - delta <= diff <= energy + delta:
                    arrows = 'set arrow from {0},{1:.5f} to {0},{2:.5f} {3}'\
                             .format(kpt + 1, orig - offset, targ - offset, append)
                    info = '{0:0>9.6f} eV | kpt: {1:0>3d} | '\
                           'bands: {2:0>2d}->{3:0>2d}'\
                           .format(diff, kpt + 1, start, finish)
                    if targ > efermi:
                        suffix = " +efermi\n"
                    else:
                        suffix = "\n"
                    text.append(arrows + ' # ' + info + suffix)
    return ''.join(text)


print('Calculating transitions for {0} around {1} eV with a delta of {2}'
      .format(ARGS.input, ARGS.energy, ARGS.delta))

ARROWFILE = 'gnuplotarrows'
EIGEN = np.loadtxt(ARGS.input)
TRANS = gentrans(EIGEN, ARGS.valence,
                        ARGS.energy,
                        ARGS.delta,
                        ARGS.efermi,
                        ARGS.offset,
                        ARGS.append)

print('Writing ===> {0}'.format(ARROWFILE))
with open(ARROWFILE, 'w') as outfile:
    print(TRANS, file=outfile)


