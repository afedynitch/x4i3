# x4i3 - The EXFOR Interface [for Python 3]

This package `x4i3` is a fork of the original `x4i` developed by David A. Brown (LLNL, Livermore CA, 94550). This pure python software acts as an interface to [Experimental Nuclear Reaction Data (EXFOR)](https://www-nds.iaea.org/exfor/), mainatined by the [International Atomic Energy Agency (IAEA)](https://www-nds.iaea.org/nrdc/). 

The database is a maintained collection of experimental and evaluated nuclear data files in the EXFOR format (*.x4), a structured markup language. The mark-up language is quite complex and the data has legacy issues, such as data sets entered by hand or issues with the strict alignment criteria of FORTRAN-era punch cards. The documentation by David A. Brown describes this code in details. Please use this [documentation](doc/x4i/x4i.pdf), the references therein and the other files in the [doc](doc) folder.

This fork emerged originally in 2016 when we tried to benchmark present photo-nuclear interaction codes against experimental data for Ultra-High Energy Cosmic Ray applications. The [resulting paper can be found here](https://www.nature.com/articles/s41598-017-05120-7) and is available as an open-access publication. The original x4i required some corrections and additions to act as a backend for an interactive application [EXFOR-chart](https://github.com/afedynitch/EXFOR-chart), that produces Figure 1 from the paper. When a box is clicked x4i helps to gathers the available data in EXFOR and to visualize it against pre-computed model predictions.

The main purpose of this fork is to ensure that such a valuable (albeit overly complex) tool stays available for the next generations, since Nuclear Engineering related webpages are often outdated, not well maintained, randomly classified etc. Or, some codes (without saying names) promise to be a great help but in practice appear as over-engineered, stuck in the technology of the 90s and badly maintained behemoths. Secondly, the original link for this code is dead and Python 2 is deprecated. Also, today we like comfortable data science, pip install everything on any architecture and environment. And this is where I see my part in this project. I hope that x4i3 can serve as a valuable tool for different branches of science and helps you to walk through the jungle of the nuclear physics heritage.

This code is distributed as it is, without any warranty or guaranty for proper operations. The full disclaimer and license information is located in the [LICENSE](LICENCE.txt). Very unfortunately, the original code is GPLv2 and hence infects in an nontransparent way all derived works such as this. Be warned!

## Requirements
- ~1 GB of hard drive space
- Python 2 or 3

## Installation::

    pip install x4i3

## Support tools

To reduce the weight of this package, the database management tools have been moved to a different project since these are for advanced users anyways.

## Documentation

There is currently no separate documentation for x4i3. Please use the original [documentation](doc/x4i/x4i.pdf).

### Authors:

*David A. Brown (LLNL)* (x4i)
*Anatoli Fedynitch* (x4i3)

## Copyright and license

Code released under [GNU General Public License (GPLv2) (see LICENSE)](LICENSE.txt).
