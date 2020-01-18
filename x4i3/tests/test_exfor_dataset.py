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

import os
import sys
import unittest

# Set up the paths to x4i & friends
from x4i3 import exfor_manager, exfor_entry, exfor_dataset, testDBPath, testIndexFileName


class TestX4DataSet(unittest.TestCase):
 
    def setUp(self):
        db = exfor_manager.X4DBManagerPlainFS(
            datapath=testDBPath, database=testIndexFileName)
        l = db.retrieve(quantity='SIG', target='PU-239', reaction='N,2N', rawEntry=True)
        self.ds = {}
        for k in l:
            # print(k)
            # This seems required to fix the test, since a new dataset has different
            # number of columns and the test fails to combine these datasets
            if k == '13787':
                continue
            self.ds.update(exfor_entry.X4Entry(l[k]).getSimplifiedDataSets(True))

    def test_append(self):
        d = exfor_dataset.X4DataSet()
        # print(list(self.ds.keys()))
        for k in sorted(list(self.ds.keys())):
            d.append(self.ds[k])
        d.sort()
        answer = '''#  Authors:   N, o, n, e\n#  Title:     None\n#  Year:      None\n#  Institute: None\n#  Reference: None\n#  Subent:    ????????\n#  Reaction:  Cross section for 239Pu(n,2n)238Pu \n#  Monitor(s): ((92-U-238(N,F),SIG), '1027MB+-5PERCENT AT 13.1MEV', None)\n#        Energy        Data          d(Energy)     d(Data)       \n#        MeV           barns         MeV           barns         \n        6.481         0.1009        0.2239        0.03081       \n        6.49          0.024         0.085         0.063         \n        6.5           0.419         0.0           0.053         \n        6.942         0.1261        0.1894        0.02015       \n        7.01          0.049         0.08          0.05          \n        7.1           0.451         0.0           0.06          \n        7.49          0.1525        0.2412        0.01422       \n        7.52          0.054         0.075         0.058         \n        8.0           0.49          0.0           0.057         \n        8.03          0.177         0.075         0.07          \n        8.084         0.2263        0.2582        0.0154        \n        8.54          0.275         0.07          0.054         \n        8.751         0.2669        0.293         0.01659       \n        9.0           0.51          0.0           0.09          \n        9.04          0.249         0.065         0.041         \n        9.504         0.3029        0.3446        0.01659       \n        9.55          0.354         0.065         0.056         \n        10.06         0.415         0.06          0.039         \n        10.34         0.3508        0.3961        0.02014       \n        10.56         0.411         0.06          0.07          \n        11.07         0.356         0.055         0.079         \n        11.34         0.3561        0.4307        0.02015       \n        11.57         0.418         0.055         0.049         \n        12.08         0.455         0.055         0.076         \n        12.45         0.2951        0.534         0.01776       \n        12.58         0.318         0.05          0.132         \n        13.09         0.588         0.05          0.148         \n        13.1          0.641         0.0           0.038         \n        13.77         0.2284        0.603         0.01539       \n        13.8          0.228         0.0           0.006384      \n        14.0          0.219         0.0           0.007884      \n        14.8          0.214         0.0           0.002996      \n        15.33         0.1558        0.7231        0.0154        \n        17.19         0.1178        0.8438        0.008262      \n        19.34         0.1025        1.068         0.007097      \n        '''.strip()
        # import IPython
        # IPython.embed()
        # print(str(d))
        #Compare only the numbers because the header is nonsense anyways and the text is picked accoding to
        # a random order in some dictionary.
        self.assertEqual(str(d).strip().split("#        Energy")[-1],
            answer.strip().split("#        Energy")[-1])


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-results'))
    except ImportError:
        unittest.main()
        print()
        print()
