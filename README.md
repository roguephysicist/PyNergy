pynergy.py
==============

```sh
usage: pynergy.py [-h] -i INPUT [-o OUTPUT] [-c] -e ENERGY [-d DELTA] [-g]
```

![](bands.png)

This script calculates transition energies between energy bands using
eigen-energy files generated by ABINIT during a band structure calculation.
This script allows you to input a desired energy value and finds all the
upward transitions that can produce that value within a specified tolerance.

If the input file is an unformatted EIG file produced by ABINIT, you can run
the script with the '-c' flag and it will automatically format it to a
plottable file and calculate the transitions.

It can also output Gnuplot arrow codes for plotting or descriptive text 
for each transition.

You can generate the sample output with 

```
./pynergy.py -c -i sample_EIG -o sample_out -e 6.81
```

A good gnuplot arrow style can be

```
set style arrow 3 head linetype 1 linecolor rgb "#000" linewidth 1.5 size screen 0.01,7,90
```

To-Do
--------
* For Gnuplot arrows, filter out duplicate lines.
* Add probability factors for different transitions.