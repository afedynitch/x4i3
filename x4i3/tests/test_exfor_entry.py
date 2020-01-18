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
from x4i3 import exfor_entry
from x4i3 import exfor_subentry
from x4i3 import exfor_section
from x4i3.tests import __path__

test_entry = (
    ''.join(
        open(
            __path__[0] +
            os.sep +
            'E0783.x4',
            mode='r').readlines())).replace(
                '\r',
    '')
test_bib = '''BIB                 10         19\nTITLE       ACCELERATION OF PROTONS AND DEUTERONS POLARIZED IN\n            THE HORIZONTAL PLANEBY THE RCNP CYCLOTRON\nAUTHOR     (K.HATANAKA,N.MATSUOKA,H.SAKAI,T.SAITO,H.TAMURA,\n           K.HOSONO,M.KONDO,K.IMAI,H.SHIMIZU,K.NISHIMURA)\nINSTITUTE  (2JPNOSA) RESEARCH CENTER FOR NUCLEAR PHYSICS, OSAKA\n            UNIV.\n           (2JPNKTO)\nREFERENCE  (J,NIM,217,397,1983)\nFACILITY   (CYCLO,2JPNOSA)\nINC-SOURCE  BEAM-INTENSITY IS 0.5NA\n            BEAM-POLARIZATION IS NOT GIVEN\n           (ATOMI) with a Wien filter\nSAMPLE      TARGET IS NOT POLARIZED\n            TARGET IS NOT ALIGNED\nPART-DET   (D)\nSTATUS     (CURVE) DATA TAKEN FROM GRAPH\nHISTORY    (19881027T) CONVERTED FROM NRDF DATA NO. D783\n           (20040401A) Author's name is corrected. Code is added\n                       into INC-SOURCE. E-EXC=0.0 MeV is deleted.\nENDBIB              19'''
test_common = '''COMMON               1          1\nEN         \nMEV        \n56.        \nENDCOMMON            3'''
test_entry_2 = (
    ''.join(
        open(
            __path__[0] +
            os.sep +
            '12898.x4',
            mode='r').readlines())).replace(
                '\r',
    '')
test_data = '''DATA                10         18
EN         EN-RSL-FW  DATA      1ERR-S      ERR-1     1ERR-T     1
MONIT     2MONIT-ERR 2DATA      2ERR-T     2
MEV        MEV        NO-DIM     PER-CENT   PER-CENT   PER-CENT
MB         PER-CENT   MB         PER-CENT
 2.856      0.095      9.075  -06 47.9       15.6       50.4
 528.8      3.0        0.004799   50.5
 2.957      0.094      1.966  -05 20.6        9.2       22.6
 524.4      3.0        0.01031    22.8
 3.057      0.094      2.575  -05 15.9       20.1       25.6
 522.7      2.5        0.01346    25.7
 3.158      0.092      7.369  -05  6.7       15.5       16.9
 524.2      2.5        0.03863    17.1
 3.258      0.090      1.441  -04  4.9       11.2       12.2
 526.7      2.5        0.07588    12.5
 3.359      0.087      2.354  -04  3.6        8.1        8.9
 529.2      2.5        0.1246      9.2
 3.459      0.087      3.210  -04  3.4        6.7        7.5
 531.7      2.5        0.1707      7.9
 3.560      0.087      4.130  -04  3.2        7.8        8.4
 536.1      2.5        0.2214      8.8
 3.661      0.087      6.140  -04  3.0        7.2        7.8
 541.7      2.5        0.3326      8.2
 3.761      0.082      7.917  -04  2.9        8.4        8.9
 544.3      2.5        0.4309      9.2
 3.861      0.084      1.281  -03  2.8        5.9        6.5
 544.9      2.5        0.6979      7.0
 3.861      0.084      1.282  -03  2.8        5.9        6.5
 544.9      2.5        0.6986      7.0
 3.962      0.081      1.348  -03  2.8        4.9        5.6
 545.5      2.5        0.7353      6.1
 4.063      0.081      1.552  -03  2.8        5.1        5.8
 546.3      2.4        0.8476      6.3
 4.264      0.075      1.967  -03  2.7        6.7        7.2
 547.4      2.4        1.007       7.6
 4.464      0.076      2.692  -03  2.7        5.2        5.9
 549.0      2.4        1.478       6.4
 4.664      0.076      4.136  -03  2.8        4.7        5.5
 544.0      2.4        2.250       6.0
 4.865      0.076      4.996  -03  2.8        4.8        5.6
 537.6      2.4        2.686       6.1
ENDDATA             40'''


class TestX4Entry(unittest.TestCase):
    def setUp(self):
        self.entry = []
        this_subent = ''
        for line in test_entry.split('\n'):
            if line.startswith('ENTRY'):
                pass
            elif line.startswith('ENDENTRY'):
                pass
            elif line.startswith('ENDSUBENT'):
                this_subent += line + '\n'
                self.entry.append(this_subent)
                this_subent = ''
            else:
                this_subent += line + '\n'
        self.entry_2 = []
        this_subent = ''
        for line in test_entry_2.split('\n'):
            if line.startswith('ENTRY'):
                pass
            elif line.startswith('ENDENTRY'):
                pass
            elif line.startswith('ENDSUBENT'):
                this_subent += line + '\n'
                self.entry_2.append(this_subent)
                this_subent = ''
            else:
                this_subent += line + '\n'

    def test_init(self):
        exfor_entry.X4Entry(self.entry)
        self.assertTrue(True)
#    def test_str( self ):
#        e = exfor_entry.X4Entry( self.entry )
#        #open( 'a', mode='w' ).writelines( test_entry )
#        #open( 'b', mode='w' ).writelines( str( e ) )
#        self.assertEqual( str( e ), test_entry )

    def test_getitem_getbib(self):
        self.assertEqual(repr(exfor_entry.X4Entry(self.entry)[1]['BIB']), test_bib)

    def test_getitem_getcommon(self):
        common = exfor_entry.X4Entry(self.entry)[1]['COMMON']
        #open( 'a', mode='w' ).writelines( test_common )
        #open( 'b', mode='w' ).writelines( str( common ) )
        self.assertEqual(repr(common), test_common)

    def test_meta(self):
        #open( 'a', mode='w' ).writelines( exfor_entry.X4Entry( self.entry ).meta().xmgrace_header() )
        # open( 'b', mode='w' ).writelines( '#Exfor Entry E0783\n#  Authors:
        # K.Hatanaka, N.Matsuoka, H.Sakai, T.Saito, H.Tamura, K.Hosono, M.Kondo,
        # K.Imai, H.Shimizu, K.Nishimura\n#  Title:     Acceleration Of Protons
        # And Deuterons Polarized In The Horizontal Planeby The Rcnp Cyclotron\n#
        # Year:      1983\n#  Institute: Osaka Univ., Osaka (Research Center For
        # Nuclear Physics, Osaka Univ.); Kyoto Univ.\n#  Reference: Nuclear
        # Instrum.and Methods in Physics Res. 217, 397 (1983)' )
        self.assertEqual(
            exfor_entry.X4Entry(
                self.entry).meta().xmgraceHeader(),
            '#Exfor Entry E0783\n#  Authors:   K.Hatanaka, N.Matsuoka, H.Sakai, T.Saito, H.Tamura, K.Hosono, M.Kondo, K.Imai, H.Shimizu, K.Nishimura\n#  Title:     Acceleration Of Protons And Deuterons Polarized In The Horizontal Planeby The Rcnp Cyclotron\n#  Year:      1983\n#  Institute: Osaka Univ., Osaka (Research Center For Nuclear Physics, Osaka Univ.); Kyoto Univ.\n#  Reference: Nuclear Instrum.and Methods in Physics Res. 217, 397 (1983)\n#  Subent:    E0783001')
        self.assertEqual(
            exfor_entry.X4Entry(
                self.entry).meta().legend(),
            '(1983) K.Hatanaka, N.Matsuoka, et al.')
        self.assertEqual(
            exfor_entry.X4Entry(
                self.entry)[1]['BIB'].meta(
                subent='E0783001').legend(),
            '(1983) K.Hatanaka, N.Matsuoka, et al.')
        self.assertEqual(
            exfor_entry.X4Entry(
                self.entry).meta().citation(),
            'K.Hatanaka, N.Matsuoka, et al., Nuclear Instrum.and Methods in Physics Res. 217, 397 (1983);  Data taken from the EXFOR database, file EXFOR E0783001 dated 1983, retrieved from the IAEA Nuclear Data Services website.')

    def test_getDataSets(self):
        ds = exfor_entry.X4Entry(self.entry).getDataSets()
        self.assertEqual(dict([(k, v.legend()) for (k, v) in ds.items()]), {
                         ('E0783', 'E0783002', ' '): '(1983) K.Hatanaka, N.Matsuoka, et al.'})
        ds[('E0783', 'E0783002', ' ')].csv('junk3.csv')
        self.assertEqual(open('junk3.csv').readlines(),
                         ['EN,ANG-CM,DATA,DATA-ERR,FLAG\n',
                          'MEV,ADEG,NO-DIM,NO-DIM,NO-DIM\n',
                          '56.0,30.712,-0.002211,,1.0\n',
                          '56.0,38.727,-0.005861,0.00821,\n',
                          '56.0,46.135,0.01022,,1.0\n',
                          '56.0,55.814,0.04098,,1.0\n',
                          '56.0,64.866,0.07998,,1.0\n',
                          '56.0,69.415,0.1126,,1.0\n',
                          '56.0,74.316,0.1633,0.0147,\n',
                          '56.0,79.924,0.2517,0.0115,\n',
                          '56.0,84.442,0.2663,0.0131,\n',
                          '56.0,89.661,0.3153,0.00821,\n',
                          '56.0,94.181,0.3315,0.0164,\n',
                          '56.0,99.114,0.4003,0.0115,\n',
                          '56.0,104.318,0.4411,0.0131,\n',
                          '56.0,109.841,0.4802,0.0132,\n',
                          '56.0,115.135,0.388,0.0132,\n',
                          '56.0,120.355,0.2531,0.0131,\n',
                          '56.0,125.595,-0.05416,0.0214,\n',
                          '56.0,129.34,-0.299,0.0197,\n',
                          '56.0,134.447,-0.314,0.018,\n',
                          '56.0,139.629,-0.1024,0.0197,\n',
                          '56.0,145.538,-0.02551,0.0148,\n',
                          '56.0,150.255,0.104,0.0246,\n',
                          '56.0,155.357,0.0857,0.0246,\n',
                          '56.0,160.562,0.1265,0.0197,\n'])
        os.remove('junk3.csv')
        answer = '#  Authors:   K.Hatanaka, N.Matsuoka, H.Sakai, T.Saito, H.Tamura, K.Hosono, M.Kondo, K.Imai, H.Shimizu, K.Nishimura\n#  Title:     Acceleration Of Protons And Deuterons Polarized In The Horizontal Planeby The Rcnp Cyclotron\n#  Year:      1983\n#  Institute: Osaka Univ., Osaka (Research Center For Nuclear Physics, Osaka Univ.); Kyoto Univ.\n#  Reference: Nuclear Instrum.and Methods in Physics Res. 217, 397 (1983)\n#  Subent:    E0783002\n#  Reaction:  Vector analyzing power, A(y), for incident beam Spin-polarization probability d/dA for 1H(d,Elastic)1H \n#        EN            ANG-CM        DATA          DATA-ERR      FLAG          \n#        MEV           ADEG          NO-DIM        NO-DIM        NO-DIM        \n        56.0          30.712        -0.002211     None          1.0           \n        56.0          38.727        -0.005861     0.00821       None          \n        56.0          46.135        0.01022       None          1.0           \n        56.0          55.814        0.04098       None          1.0           \n        56.0          64.866        0.07998       None          1.0           \n        56.0          69.415        0.1126        None          1.0           \n        56.0          74.316        0.1633        0.0147        None          \n        56.0          79.924        0.2517        0.0115        None          \n        56.0          84.442        0.2663        0.0131        None          \n        56.0          89.661        0.3153        0.00821       None          \n        56.0          94.181        0.3315        0.0164        None          \n        56.0          99.114        0.4003        0.0115        None          \n        56.0          104.318       0.4411        0.0131        None          \n        56.0          109.841       0.4802        0.0132        None          \n        56.0          115.135       0.388         0.0132        None          \n        56.0          120.355       0.2531        0.0131        None          \n        56.0          125.595       -0.05416      0.0214        None          \n        56.0          129.34        -0.299        0.0197        None          \n        56.0          134.447       -0.314        0.018         None          \n        56.0          139.629       -0.1024       0.0197        None          \n        56.0          145.538       -0.02551      0.0148        None          \n        56.0          150.255       0.104         0.0246        None          \n        56.0          155.357       0.0857        0.0246        None          \n        56.0          160.562       0.1265        0.0197        None          \n        '
        #open( 'a', mode='w' ).writelines( str( ds[ ('E0783', 'E0783002', ' ') ] ) )
        #open( 'b', mode='w' ).writelines( answer )
        self.assertEqual(str(ds[('E0783', 'E0783002', ' ')]), answer)

    def test_getDataSets_2(self):
        ds = exfor_entry.X4Entry(self.entry_2).getDataSets()
        self.assertEqual(dict([(k,
                                v.legend()) for (k,
                                                 v) in ds.items()]),
                         {('12898',
                           '12898003',
                           '2'): '(1984) D.L.Smith, J.W.Meadows, et al.',
                          ('12898',
                           '12898002',
                           '2'): '(1984) D.L.Smith, J.W.Meadows, et al.',
                          ('12898',
                             '12898002',
                             '1'): '(1984) D.L.Smith, J.W.Meadows, et al.',
                          ('12898',
                             '12898003',
                             '1'): '(1984) D.L.Smith, J.W.Meadows, et al.'})
        ds[('12898', '12898003', '2')].csv('junk4.csv')
        self.assertEqual(open('junk4.csv').readlines(),
                         ['EN,EN-RSL-FW,ERR-S,MONIT,MONIT-ERR,DATA,ERR-T\n',
                          'MEV,MEV,PER-CENT,MB,PER-CENT,MB,PER-CENT\n',
                          '4.643,0.276,2.7,544.7,2.4,2.236,6.3\n',
                          '4.893,0.248,2.6,536.8,2.4,2.853,7.1\n',
                          '5.139,0.211,2.4,537.3,2.6,3.25,6.3\n',
                          '5.374,0.194,2.4,543.9,2.6,3.642,6.1\n',
                          '5.6,0.18,2.4,560.4,2.6,4.243,6.6\n',
                          '5.819,0.174,2.4,589.0,2.6,5.041,6.4\n',
                          '5.822,0.167,2.5,589.4,2.6,5.228,6.4\n',
                          '6.04,0.162,2.3,627.4,3.9,6.023,6.7\n',
                          '6.254,0.153,2.3,710.0,3.9,7.142,6.6\n',
                          '6.465,0.146,2.3,796.7,3.9,7.517,6.5\n',
                          '6.675,0.149,2.3,860.0,3.9,8.013,6.5\n',
                          '6.881,0.144,2.3,904.9,3.9,9.077,6.4\n',
                          '6.882,0.141,2.3,905.1,3.9,9.023,6.4\n',
                          '7.087,0.141,2.3,933.2,3.9,9.362,6.4\n',
                          '7.29,0.144,2.3,959.7,3.9,10.45,6.4\n',
                          '7.494,0.144,2.6,986.3,3.9,11.66,6.6\n',
                          '7.694,0.152,2.5,988.6,3.9,11.72,6.5\n',
                          '7.893,0.155,2.9,990.1,3.9,12.72,6.7\n',
                          '7.893,0.156,2.9,990.1,3.9,13.24,6.7\n',
                          '8.092,0.161,2.9,991.7,2.9,13.2,6.1\n',
                          '8.29,0.169,2.9,993.1,2.9,13.93,6.1\n',
                          '8.486,0.173,3.3,994.6,2.9,14.44,6.3\n',
                          '8.683,0.181,3.3,996.0,2.9,15.65,6.4\n',
                          '8.684,0.179,3.3,996.0,2.9,15.72,6.3\n',
                          '8.879,0.184,3.4,997.5,2.9,15.94,6.3\n',
                          '9.071,0.189,3.8,997.3,2.9,17.73,6.7\n',
                          '9.267,0.195,3.8,994.0,2.9,18.39,6.7\n'])
        os.remove('junk4.csv')
        answer = '#  Authors:   D.L.Smith, J.W.Meadows, I.Kanno\n#  Title:     Measured Activation Cross Sections Below 10 Mev For The 51-V(N,P)51-Ti And 51-V(N,Alpha)48-Sc Reactions.\n#  Year:      1984\n#  Institute: Argonne National Laboratory, Argonne, IL\n#  Reference: Annals of Nuclear Energy 11, 623 (1984); Progress report: ANL-NDM-85  (1984)\n#  Subent:    12898002\n#  Reaction:  (( Cross section for 51V(n,p)51Ti )/( Cross section for 238U(n,Fission) )) \n#        EN            EN-RSL-FW     DATA          ERR-S         ERR-1         ERR-T         \n#        MEV           MEV           NO-DIM        PER-CENT      PER-CENT      PER-CENT      \n        2.856         0.095         9.075e-06     47.9          15.6          50.4          \n        2.957         0.094         1.966e-05     20.6          9.2           22.6          \n        3.057         0.094         2.575e-05     15.9          20.1          25.6          \n        3.158         0.092         7.369e-05     6.7           15.5          16.9          \n        3.258         0.09          0.0001441     4.9           11.2          12.2          \n        3.359         0.087         0.0002354     3.6           8.1           8.9           \n        3.459         0.087         0.000321      3.4           6.7           7.5           \n        3.56          0.087         0.000413      3.2           7.8           8.4           \n        3.661         0.087         0.000614      3.0           7.2           7.8           \n        3.761         0.082         0.0007917     2.9           8.4           8.9           \n        3.861         0.084         0.001281      2.8           5.9           6.5           \n        3.861         0.084         0.001282      2.8           5.9           6.5           \n        3.962         0.081         0.001348      2.8           4.9           5.6           \n        4.063         0.081         0.001552      2.8           5.1           5.8           \n        4.264         0.075         0.001967      2.7           6.7           7.2           \n        4.464         0.076         0.002692      2.7           5.2           5.9           \n        4.664         0.076         0.004136      2.8           4.7           5.5           \n        4.865         0.076         0.004996      2.8           4.8           5.6           \n        '
        #open( 'a', mode='w' ).writelines( str( ds[ ('12898', '12898002', '1') ] ) )
        #open( 'b', mode='w' ).writelines( answer )
        self.assertEqual(str(ds[('12898', '12898002', '1')]), answer)

    def test_getDataSets_2_cross_section_translation(self):
        ds = exfor_entry.X4Entry(self.entry_2).getSimplifiedDataSets()
        self.assertEqual(dict([(k,
                                v.legend()) for (k,
                                                 v) in ds.items()]),
                         {('12898',
                           '12898003',
                           '2'): '(1984) D.L.Smith, J.W.Meadows, et al.',
                          ('12898',
                           '12898002',
                           '2'): '(1984) D.L.Smith, J.W.Meadows, et al.',
                          ('12898',
                             '12898002',
                             '1'): '(1984) D.L.Smith, J.W.Meadows, et al.',
                          ('12898',
                             '12898003',
                             '1'): '(1984) D.L.Smith, J.W.Meadows, et al.'})
        ds[('12898', '12898003', '2')].csv('junk5.csv')
        left = open('junk5.csv').readlines()
        right = [
            'Energy,Data,d(Energy),d(Data)\n',
            'MeV,barns,MeV,barns\n',
            '4.643,0.002236,0.138,0.000140868\n',
            '4.893,0.002853,0.124,0.000202563\n',
            '5.139,0.00325,0.1055,0.00020475\n',
            '5.374,0.003642,0.097,0.000222162\n',
            '5.6,0.004243,0.09,0.000280038\n',
            '5.819,0.005041,0.087,0.000322624\n',
            '5.822,0.005228,0.0835,0.000334592\n',
            '6.04,0.006023,0.081,0.000403541\n',
            '6.254,0.007142,0.0765,0.000471372\n',
            '6.465,0.007517,0.073,0.000488605\n',
            '6.675,0.008013,0.0745,0.000520845\n',
            '6.881,0.009077,0.072,0.000580928\n',
            '6.882,0.009023,0.0705,0.000577472\n',
            '7.087,0.009362,0.0705,0.000599168\n',
            '7.29,0.01045,0.072,0.0006688\n',
            '7.494,0.01166,0.072,0.00076956\n',
            '7.694,0.01172,0.076,0.0007618\n',
            '7.893,0.01272,0.0775,0.00085224\n',
            '7.893,0.01324,0.078,0.00088708\n',
            '8.092,0.0132,0.0805,0.0008052\n',
            '8.29,0.01393,0.0845,0.00084973\n',
            '8.486,0.01444,0.0865,0.00090972\n',
            '8.683,0.01565,0.0905,0.0010016\n',
            '8.684,0.01572,0.0895,0.00099036\n',
            '8.879,0.01594,0.092,0.00100422\n',
            '9.071,0.01773,0.0945,0.00118791\n',
            '9.267,0.01839,0.0975,0.00123213\n']
        self.assertEqual(len(left), len(right))
        self.assertEqual(left[:2], right[:2])
        for i in range(2, len(left)):
            leftRow = list(map(float, left[i].split(',')))
            rightRow = list(map(float, right[i].split(',')))
            for j in range(len(leftRow)):
                self.assertAlmostEqual(leftRow[j], rightRow[j])
        os.remove('junk5.csv')
        answer = '#  Authors:   D.L.Smith, J.W.Meadows, I.Kanno\n#  Title:     Measured Activation Cross Sections Below 10 Mev For The 51-V(N,P)51-Ti And 51-V(N,Alpha)48-Sc Reactions.\n#  Year:      1984\n#  Institute: Argonne National Laboratory, Argonne, IL\n#  Reference: Annals of Nuclear Energy 11, 623 (1984); Progress report: ANL-NDM-85  (1984)\n#  Subent:    12898002\n#  Reaction:  (( Cross section for 51V(n,p)51Ti )/( Cross section for 238U(n,Fission) )) \n#        Energy        Data          d(Energy)     d(Data)       \n#        MeV           no-dim        MeV           no-dim        \n        2.856         9.075e-06     0.0475        4.5738e-06    \n        2.957         1.966e-05     0.047         4.44316e-06   \n        3.057         2.575e-05     0.047         6.592e-06     \n        3.158         7.369e-05     0.046         1.245361e-05  \n        3.258         0.0001441     0.045         1.75802e-05   \n        3.359         0.0002354     0.0435        2.09506e-05   \n        3.459         0.000321      0.0435        2.4075e-05    \n        3.56          0.000413      0.0435        3.4692e-05    \n        3.661         0.000614      0.0435        4.7892e-05    \n        3.761         0.0007917     0.041         7.04613e-05   \n        3.861         0.001281      0.042         8.3265e-05    \n        3.861         0.001282      0.042         8.333e-05     \n        3.962         0.001348      0.0405        7.5488e-05    \n        4.063         0.001552      0.0405        9.0016e-05    \n        4.264         0.001967      0.0375        0.000141624   \n        4.464         0.002692      0.038         0.000158828   \n        4.664         0.004136      0.038         0.00022748    \n        4.865         0.004996      0.038         0.000279776   \n        '
        #open( 'a', mode='w' ).writelines( str( ds[ ('12898', '12898002', '1') ] ) )
        #open( 'b', mode='w' ).writelines( answer )
        self.assertEqual(str(ds[('12898', '12898002', '1')]), answer)


class TestX4BibSection(unittest.TestCase):
    def test_init(self):
        exfor_section.X4BibSection(test_bib.split('\n'))
        self.assertTrue(True)

    def test_repr(self):
        bib = exfor_section.X4BibSection(test_bib.split('\n'))
        #open( 'a', mode='w' ).writelines( test_bib )
        #open( 'b', mode='w' ).writelines( repr( bib ) )
        self.assertEqual(repr(bib), test_bib)

    def test_total_len(self):
        self.assertEqual(exfor_section.X4BibSection(test_bib.split('\n')).totalLen(), 19)


class TestX4DataSection(unittest.TestCase):
    def test_simple_common(self):
        x4ds = exfor_section.X4DataSection('COMMON', test_common.split('\n'))
        self.assertEqual(repr(x4ds), test_common)
        self.assertEqual(
            str(x4ds),
            'COMMON               1          1\nEN         \nMEV        \n56.0       \nENDCOMMON            3')
        self.assertEqual(len(x4ds), 1)
        self.assertEqual(x4ds.pointers, {})
        x4ds.csv('junk1.csv')
        self.assertEqual(open('junk1.csv').readlines(), ['EN\n', 'MEV\n', '56.0\n'])
        os.remove('junk1.csv')
        self.assertEqual(x4ds['LABELS', 0], 'EN')
        self.assertEqual(x4ds['UNITS', 0], 'MEV')
        self.assertEqual(x4ds[0, 0], 56.0)

    def test_complicated_data(self):
        x4ds = exfor_section.X4DataSection('DATA', test_data.split('\n'))
        #open( 'a', mode='w' ).writelines( str( x4ds ) )
        #open( 'b', mode='w' ).writelines( test_data )
        self.assertEqual(str(x4ds), 'DATA                10         18\nEN         EN-RSL-FW  DATA      1ERR-S      ERR-1     1ERR-T     1MONIT     2MONIT-ERR 2DATA      2ERR-T     2\nMEV        MEV        NO-DIM     PER-CENT   PER-CENT   PER-CENT   MB         PER-CENT   MB         PER-CENT   \n2.856      0.095      9.075e-06  47.9       15.6       50.4       528.8      3.0        0.004799   50.5       \n2.957      0.094      1.966e-05  20.6       9.2        22.6       524.4      3.0        0.01031    22.8       \n3.057      0.094      2.575e-05  15.9       20.1       25.6       522.7      2.5        0.01346    25.7       \n3.158      0.092      7.369e-05  6.7        15.5       16.9       524.2      2.5        0.03863    17.1       \n3.258      0.09       0.0001441  4.9        11.2       12.2       526.7      2.5        0.07588    12.5       \n3.359      0.087      0.0002354  3.6        8.1        8.9        529.2      2.5        0.1246     9.2        \n3.459      0.087      0.000321   3.4        6.7        7.5        531.7      2.5        0.1707     7.9        \n3.56       0.087      0.000413   3.2        7.8        8.4        536.1      2.5        0.2214     8.8        \n3.661      0.087      0.000614   3.0        7.2        7.8        541.7      2.5        0.3326     8.2        \n3.761      0.082      0.0007917  2.9        8.4        8.9        544.3      2.5        0.4309     9.2        \n3.861      0.084      0.001281   2.8        5.9        6.5        544.9      2.5        0.6979     7.0        \n3.861      0.084      0.001282   2.8        5.9        6.5        544.9      2.5        0.6986     7.0        \n3.962      0.081      0.001348   2.8        4.9        5.6        545.5      2.5        0.7353     6.1        \n4.063      0.081      0.001552   2.8        5.1        5.8        546.3      2.4        0.8476     6.3        \n4.264      0.075      0.001967   2.7        6.7        7.2        547.4      2.4        1.007      7.6        \n4.464      0.076      0.002692   2.7        5.2        5.9        549.0      2.4        1.478      6.4        \n4.664      0.076      0.004136   2.8        4.7        5.5        544.0      2.4        2.25       6.0        \n4.865      0.076      0.004996   2.8        4.8        5.6        537.6      2.4        2.686      6.1        \nENDDATA             20')
        self.assertEqual(repr(x4ds), 'DATA                10         18\nEN         EN-RSL-FW  DATA      1ERR-S      ERR-1     1ERR-T     1MONIT     2MONIT-ERR 2DATA      2ERR-T     2\nMEV        MEV        NO-DIM     PER-CENT   PER-CENT   PER-CENT   MB         PER-CENT   MB         PER-CENT   \n2.856      0.095      9.075  -06 47.9       15.6       50.4       528.8      3.0        0.004799   50.5       \n2.957      0.094      1.966  -05 20.6       9.2        22.6       524.4      3.0        0.01031    22.8       \n3.057      0.094      2.575  -05 15.9       20.1       25.6       522.7      2.5        0.01346    25.7       \n3.158      0.092      7.369  -05 6.7        15.5       16.9       524.2      2.5        0.03863    17.1       \n3.258      0.090      1.441  -04 4.9        11.2       12.2       526.7      2.5        0.07588    12.5       \n3.359      0.087      2.354  -04 3.6        8.1        8.9        529.2      2.5        0.1246     9.2        \n3.459      0.087      3.210  -04 3.4        6.7        7.5        531.7      2.5        0.1707     7.9        \n3.560      0.087      4.130  -04 3.2        7.8        8.4        536.1      2.5        0.2214     8.8        \n3.661      0.087      6.140  -04 3.0        7.2        7.8        541.7      2.5        0.3326     8.2        \n3.761      0.082      7.917  -04 2.9        8.4        8.9        544.3      2.5        0.4309     9.2        \n3.861      0.084      1.281  -03 2.8        5.9        6.5        544.9      2.5        0.6979     7.0        \n3.861      0.084      1.282  -03 2.8        5.9        6.5        544.9      2.5        0.6986     7.0        \n3.962      0.081      1.348  -03 2.8        4.9        5.6        545.5      2.5        0.7353     6.1        \n4.063      0.081      1.552  -03 2.8        5.1        5.8        546.3      2.4        0.8476     6.3        \n4.264      0.075      1.967  -03 2.7        6.7        7.2        547.4      2.4        1.007      7.6        \n4.464      0.076      2.692  -03 2.7        5.2        5.9        549.0      2.4        1.478      6.4        \n4.664      0.076      4.136  -03 2.8        4.7        5.5        544.0      2.4        2.250      6.0        \n4.865      0.076      4.996  -03 2.8        4.8        5.6        537.6      2.4        2.686      6.1        \nENDDATA             20')
        self.assertEqual(len(x4ds), 18)
        self.assertEqual(x4ds.pointers, {'1': [2, 4, 5], '2': [6, 7, 8, 9]})
        x4ds.csv('junk2.csv')
        self.assertEqual(
            open('junk2.csv').readlines(),
            [
                'EN,EN-RSL-FW,DATA      1,ERR-S,ERR-1     1,ERR-T     1,MONIT     2,MONIT-ERR 2,DATA      2,ERR-T     2\n',
                'MEV,MEV,NO-DIM,PER-CENT,PER-CENT,PER-CENT,MB,PER-CENT,MB,PER-CENT\n',
                '2.856,0.095,9.075e-06,47.9,15.6,50.4,528.8,3.0,0.004799,50.5\n',
                '2.957,0.094,1.966e-05,20.6,9.2,22.6,524.4,3.0,0.01031,22.8\n',
                '3.057,0.094,2.575e-05,15.9,20.1,25.6,522.7,2.5,0.01346,25.7\n',
                '3.158,0.092,7.369e-05,6.7,15.5,16.9,524.2,2.5,0.03863,17.1\n',
                '3.258,0.09,0.0001441,4.9,11.2,12.2,526.7,2.5,0.07588,12.5\n',
                '3.359,0.087,0.0002354,3.6,8.1,8.9,529.2,2.5,0.1246,9.2\n',
                '3.459,0.087,0.000321,3.4,6.7,7.5,531.7,2.5,0.1707,7.9\n',
                '3.56,0.087,0.000413,3.2,7.8,8.4,536.1,2.5,0.2214,8.8\n',
                '3.661,0.087,0.000614,3.0,7.2,7.8,541.7,2.5,0.3326,8.2\n',
                '3.761,0.082,0.0007917,2.9,8.4,8.9,544.3,2.5,0.4309,9.2\n',
                '3.861,0.084,0.001281,2.8,5.9,6.5,544.9,2.5,0.6979,7.0\n',
                '3.861,0.084,0.001282,2.8,5.9,6.5,544.9,2.5,0.6986,7.0\n',
                '3.962,0.081,0.001348,2.8,4.9,5.6,545.5,2.5,0.7353,6.1\n',
                '4.063,0.081,0.001552,2.8,5.1,5.8,546.3,2.4,0.8476,6.3\n',
                '4.264,0.075,0.001967,2.7,6.7,7.2,547.4,2.4,1.007,7.6\n',
                '4.464,0.076,0.002692,2.7,5.2,5.9,549.0,2.4,1.478,6.4\n',
                '4.664,0.076,0.004136,2.8,4.7,5.5,544.0,2.4,2.25,6.0\n',
                '4.865,0.076,0.004996,2.8,4.8,5.6,537.6,2.4,2.686,6.1\n'])
        os.remove('junk2.csv')
        self.assertEqual(x4ds['LABELS', 2], 'DATA      1')
        self.assertEqual(x4ds['UNITS', 9], 'PER-CENT')
        self.assertEqual(x4ds[10, 7], 2.5)


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-results'))
    except ImportError:
        unittest.main()
        print()
        print()
