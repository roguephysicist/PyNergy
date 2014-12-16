#!/Users/sma/anaconda/bin/python
"""
A script for calculating transition energies between bands.
"""

import sys
import numpy as np

INPUT = sys.argv[1]
#OUTPUT = sys.argv[2]
TARGET = float(sys.argv[2])
ERROR = 0.1

EIGEN = np.loadtxt(INPUT)
KPTS = len(EIGEN)
BANDS = len(EIGEN[0])

#FILE = open(OUTPUT, 'w')
energies = []
kpoints = []
borigin = []
btarget = []
seta = []

#for kpt in range(0, KPTS):
for kpt in range(0, 1):
    for start in range(1, BANDS):
        for finish in range(start + 1, BANDS):
            diff = abs(EIGEN[kpt, start] - EIGEN[kpt, finish])
            seta.append(TARGET - ERROR <= diff <= TARGET + ERROR)
            energies.append(diff)
            kpoints.append(kpt)
            borigin.append(start)
            btarget.append(finish)
print seta
x = np.array((energies, kpoints, borigin, btarget))
            #entry = '{0:0>3d}.{1:0>2d}->{2:0>2d}'.format(kpt + 1, start, finish)
            #value = '{0:0>9.6f}'.format(diff)
            #result = '{1:0>9.6f} | ' \
            #         'k-point: {0:0>3d} | ' \
            #         'bands: {2:0>2d} -> {3:0>2d}\n' \
            #         .format(kpt + 1, diff, start, finish)
            #FILE.write(result)


#FILE.close()