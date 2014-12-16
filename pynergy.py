#!/Users/sma/anaconda/bin/python
"""
A script for calculating transition energies between bands.
"""

import sys
import numpy as np

INPUT = sys.argv[1]
OUTPUT = sys.argv[2]

EIGEN = np.loadtxt(INPUT)
KPTS = len(EIGEN)
BANDS = len(EIGEN[0])

#FILE = open(OUTPUT, 'w')
energies = []
kpoints = []
borigin = []
btarget = []

#for kpt in range(0, KPTS):
for kpt in range(0, 1):
    for origin in range(1, BANDS):
        for target in range(origin + 1, BANDS):
            diff = abs(EIGEN[kpt, origin] - EIGEN[kpt, target])
            energies.append(diff)
            kpoints.append(kpt)
            borigin.append(origin)
            btarget.append(target)
            x = np.array((energies, kpoints, borigin, btarget))
            #entry = '{0:0>3d}.{1:0>2d}->{2:0>2d}'.format(kpt + 1, origin, target)
            #value = '{0:0>9.6f}'.format(diff)
            #result = '{1:0>9.6f} | ' \
            #         'k-point: {0:0>3d} | ' \
            #         'bands: {2:0>2d} -> {3:0>2d}\n' \
            #         .format(kpt + 1, diff, origin, target)
            #FILE.write(result)

#print x
#print 0.0 <= x <= 0.5
#FILE.close()
