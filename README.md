![PyPI](https://img.shields.io/pypi/v/x4i3)
[![Build Status](https://dev.azure.com/afedynitch/NuclearTools/_apis/build/status/afedynitch.x4i3?branchName=master)](https://dev.azure.com/afedynitch/NuclearTools/_build/latest?definitionId=4&branchName=master)
![Azure DevOps releases](https://img.shields.io/azure-devops/release/afedynitch/66c7ff07-d4ed-41bb-b939-9ed4dd5d61f9/1/1)

# x4i3 - The EXFOR Interface [for Python 3]

This package `x4i3` is a fork of the original `x4i` developed by David A. Brown (LLNL, Livermore CA, 94550). This pure python software acts as an interface to [Experimental Nuclear Reaction Data (EXFOR)](https://www-nds.iaea.org/exfor/) that the [International Atomic Energy Agency (IAEA)](https://www-nds.iaea.org/nrdc/) actively maintains.

The database resembles a collection of experimental and evaluated nuclear data files in the EXFOR format (*.x4), a structured markup language. The mark-up language is quite complex and the data has legacy issues, such as data sets entered by hand or issues with the strict alignment criteria of FORTRAN-era punch cards. The documentation by David A. Brown describes a few basics of the format. Please use this [documentation](doc/x4i/x4i.pdf), the references therein and the other files in the [doc](doc) folder. Please also cite the papers about the database if you use these data in your research.

The main purpose of this fork is to ensure that such a valuable and complex tool does stays available. Also, the original link for this code is dead and Python 2 is deprecated. As a standalone pure Python package on pip, it may cure derived works from a potential GPL infection.  

### Latest release 1.2.0

Update to EXFOR database version dated 2021/03/08.

### History

This fork emerged originally in 2016 when we tried to benchmark current photo-nuclear interaction codes against experimental data in a project related to Ultra-High Energy Cosmic Rays. One paper that came out [has a quite useful plot (Figure 1)](https://www.nature.com/articles/s41598-017-05120-7). Actually, this figure is [an interactive matplotlib application](https://github.com/afedynitch/EXFOR_chart) that used the original `x4i` as a backend. When a box is clicked x4i gathers experimental data from EXFOR, applies some filtering and visualizes the data against pre-computed model predictions.

### Examples

Nothing very useful yet. To check out if the installation is successful, try:

        python examples/get-entry.py --data -s 10504002

It should print some fission cross section to stdout.

### Contributions

..are welcome. Also feel free to say hi since I don't know if there is a community who may find this interface useful.

Currently there is no development goals beyond basic maintenance.

### Requirements

- ~1 GB of hard drive space

### Installation

    pip install x4i3

Note that on first import ~600MB will be downloaded and 22k files will be decompressed to the data directory.

### Support tools

To reduce the weight of this package, the database management tools have been moved to a different project [`x4i3_tools`](https://github.com/afedynitch/x4i3_tools) since these are for advanced users anyways.

### Documentation

There is currently no separate documentation for `x4i3`. Please use the original [documentation](doc/x4i/x4i.pdf). The installation instruction are not valid anymore. There is a detailed but auto-generated [API-doc documentation](doc/x4i/). Untar and enjoy the `index.html` if you need this.

### Authors

*David A. Brown (LLNL)* (`x4i`)

*Anatoli Fedynitch* (`x4i3`)

### Copyright and license

This code is distributed under the [GNU General Public License (GPLv2) (see LICENSE)](LICENSE.txt) without any warranty or guaranty. The full disclaimer and license information is located in the [LICENSE](LICENCE.txt). Very unfortunately, the original code is GPLv2 infecting in a nontransparent way all derived works such as this. Be warned!
