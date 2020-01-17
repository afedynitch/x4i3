# Copyright (c) 2011, Lawrence Livermore National Security, LLC. Produced at
# the Lawrence Livermore National Laboratory. Written by David A. Brown
# <brown170@llnl.gov>.
#
# LLNL-CODE-484151 All rights reserved.
#
# This file is part of EXFOR Interface (x4i)
#
# Please also read the LICENSE.txt file included in this distribution, under
# "Our Notice and GNU General Public License".
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License (as published by the
# Free Software Foundation) version 2, dated June 1991.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# terms and conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from x4i3 import exfor_manager, exfor_entry
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

isotope = 'NA-23'  # 'AL-27'
reaction = 'G,N'
observable = 'CS'
outtype = 'PostScript'

if __name__ == "__main__":

    try:
        isotope = sys.argv[1].upper()
    except BaseException:
        pass
    try:
        reaction = sys.argv[2].upper()
    except BaseException:
        pass

    title = isotope.capitalize() + '(' + reaction.lower()
    outfile = '"' + title + ')' + '.' + outtype.lower() + '"'

    db = exfor_manager.X4DBManagerPlainFS()

    fileList = []
    i = 0
    subents = db.retrieve(target=isotope, reaction=reaction, quantity=observable)
    print(subents)
    print('Retrieving entries:')
    for e in subents:
        print('    Entry:', e)
        if e == '22208':
            continue
        ds = exfor_entry.X4Entry(subents[e]).getSimplifiedDataSets(makeAllColumns=True)
        for d in ds:
            print('       ', d)
            result = str(ds[d])
            fileList.append('junk' + str(i) + '.dat')
            open(fileList[-1], mode='w').writelines(result)
            i += 1
    if i == 0:
        sys.exit(1)
    command = 'xmgrace -autoscale xy -hardcopy -remove -printfile ' \
        + outfile + ' -hdevice ' + outtype + ' '\
        + ' '.join(['-settype xydxdy ' + fname for fname in fileList]) \
        + ' -saveall ' + outfile.replace(outtype.lower(), 'agr')
    print(command)
    os.system(command)
    os.system('rm -f ' + ' '.join(fileList))
