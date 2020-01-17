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
from x4i3 import exfor_manager, testDBPath, testIndexFileName

ENTRYANSWER = {
    'E0783': [
        'SUBENT        E0783001     881027\nBIB                 10         18\nTITLE       ACCELERATION OF PROTONS AND DEUTERONS POLARIZED IN\n            THE HORIZONTAL PLANEBY THE RCNP CYCLOTRON\nAUTHOR     (K.HATANAKA,N.MATSUOKA,H.SAKAI,T.SAITO,H.TAMURA,\n           K.HOSONO,M.KONDO,K.IMAI,H,SHIMIZU,K.NISHIMURA)\nINSTITUTE  (2JPNOSA) RESEARCH CENTER FOR NUCLEAR PHYSICS, OSAKA\n            UNIV.\n           (2JPNKTO)\nREFERENCE  (J,NIM,217,397,83)\nFACILITY   (CYCLO,2JPNOSA)\nINC-SOURCE  BEAM-INTENSITY IS 0.5NA\n            BEAM-POLARIZATION IS NOT GIVEN\n            ION-SOURCE=AN ATOMIC BEAM TYPE ION SOURCE WITH A\n            WIEN FILTER\nSAMPLE      TARGET IS NOT POLARIZED\n            TARGET IS NOT ALIGNED\nPART-DET   (D)\nSTATUS     (CURVE) DATA TAKEN FROM GRAPH\nHISTORY    (881027T) CONVERTED FROM NRDF DATA NO. D783\nENDBIB              18\nCOMMON               2          3\nEN         E-EXC\nMEV        MEV\n56.        0.0\nENDCOMMON            3\nENDSUBENT           25\n',
        'SUBENT        E0783002     881027\nBIB                  2          2\nREACTION   (1-H-1(D,EL)1-H-1,PAR,POL/DA,,ANA)\nFLAG       (1.) DATA ERROR IS SMALLER THAN DATA POINT\nENDBIB               2\nNOCOMMON             0          0\nDATA                 4         24\nANG-CM     DATA       DATA-ERR   FLAG\nADEG       NO-DIM     NO-DIM     NO-DIM\n     30.712 -2.211E-03                    1.\n     38.727 -5.861E-03  0.821E-02\n     46.135  1.022E-02                    1.\n     55.814  4.098E-02                    1.\n     64.866  7.998E-02                    1.\n     69.415  1.126E-01                    1.\n     74.316  1.633E-01  0.147E-01\n     79.924  2.517E-01  0.115E-01\n     84.442  2.663E-01  0.131E-01\n     89.661  3.153E-01  0.821E-02\n     94.181  3.315E-01  0.164E-01\n     99.114  4.003E-01  0.115E-01\n    104.318  4.411E-01  0.131E-01\n    109.841  4.802E-01  0.132E-01\n    115.135  3.880E-01  0.132E-01\n    120.355  2.531E-01  0.131E-01\n    125.595 -5.416E-02  0.214E-01\n    129.340 -2.990E-01  0.197E-01\n    134.447 -3.140E-01  0.180E-01\n    139.629 -1.024E-01  0.197E-01\n    145.538 -2.551E-02  0.148E-01\n    150.255  1.040E-01  0.246E-01\n    155.357  8.570E-02  0.246E-01\n    160.562  1.265E-01  0.197E-01\nENDDATA             26\nENDSUBENT           33\n']}
NEWENTRYANSWER = {'E0783': ['''SUBENT        E0783001   20040622              20050926       0000
BIB                 10         19
TITLE       ACCELERATION OF PROTONS AND DEUTERONS POLARIZED IN
            THE HORIZONTAL PLANEBY THE RCNP CYCLOTRON
AUTHOR     (K.HATANAKA,N.MATSUOKA,H.SAKAI,T.SAITO,H.TAMURA,
           K.HOSONO,M.KONDO,K.IMAI,H.SHIMIZU,K.NISHIMURA)
INSTITUTE  (2JPNOSA) RESEARCH CENTER FOR NUCLEAR PHYSICS, OSAKA
            UNIV.
           (2JPNKTO)
REFERENCE  (J,NIM,217,397,1983)
FACILITY   (CYCLO,2JPNOSA)
INC-SOURCE  BEAM-INTENSITY IS 0.5NA
            BEAM-POLARIZATION IS NOT GIVEN
           (ATOMI) with a Wien filter
SAMPLE      TARGET IS NOT POLARIZED
            TARGET IS NOT ALIGNED
PART-DET   (D)
STATUS     (CURVE) DATA TAKEN FROM GRAPH
HISTORY    (19881027T) CONVERTED FROM NRDF DATA NO. D783
           (20040401A) Author's name is corrected. Code is added
                       into INC-SOURCE. E-EXC=0.0 MeV is deleted.
ENDBIB              19
COMMON               1          3
EN
MEV
56.
ENDCOMMON            3
ENDSUBENT           26
''', '''SUBENT        E0783002   20040622              20050926       0000
BIB                  4          5
REACTION   (1-H-1(D,EL)1-H-1,SL,POL/DA,,ANA)
FLAG       (1.) DATA ERROR IS SMALLER THAN DATA POINT
ERR-ANALYS (DATA-ERR) Uncertainty scanned from figure
HISTORY    (20040401A) Quantity code is correcetd.
                       ERR-ANALYS is added.
ENDBIB               5
NOCOMMON             0          0
DATA                 4         24
ANG-CM     DATA       DATA-ERR   FLAG
ADEG       NO-DIM     NO-DIM     NO-DIM
     30.712 -2.211E-03                    1.
     38.727 -5.861E-03  0.821E-02
     46.135  1.022E-02                    1.
     55.814  4.098E-02                    1.
     64.866  7.998E-02                    1.
     69.415  1.126E-01                    1.
     74.316  1.633E-01  0.147E-01
     79.924  2.517E-01  0.115E-01
     84.442  2.663E-01  0.131E-01
     89.661  3.153E-01  0.821E-02
     94.181  3.315E-01  0.164E-01
     99.114  4.003E-01  0.115E-01
    104.318  4.411E-01  0.131E-01
    109.841  4.802E-01  0.132E-01
    115.135  3.880E-01  0.132E-01
    120.355  2.531E-01  0.131E-01
    125.595 -5.416E-02  0.214E-01
    129.340 -2.990E-01  0.197E-01
    134.447 -3.140E-01  0.180E-01
    139.629 -1.024E-01  0.197E-01
    145.538 -2.551E-02  0.148E-01
    150.255  1.040E-01  0.246E-01
    155.357  8.570E-02  0.246E-01
    160.562  1.265E-01  0.197E-01
ENDDATA             26
ENDSUBENT           36
''']}


class TestX4DBManager(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dbMgr = exfor_manager.X4DBManagerPlainFS(
            datapath=testDBPath, database=testIndexFileName)

    def test_fixkey(self):
        self.assertEqual(self.dbMgr.__fixkey__(10001), '10001')
        self.assertEqual(self.dbMgr.__fixkey__(10001015), '10001015')
        self.assertEqual(self.dbMgr.__fixkey__('10001'), '10001')
        self.assertEqual(self.dbMgr.__fixkey__('10001015'), '10001015')
        self.assertRaises(KeyError, self.dbMgr.__fixkey__, '1000101')

    def test_entry_query(self):
        self.assertEqual(self.dbMgr.query(ENTRY=10001),
                         {'10001': ['10001001',
                                    '10001002',
                                    '10001003',
                                    '10001004',
                                    '10001005',
                                    '10001006',
                                    '10001007',
                                    '10001008',
                                    '10001009',
                                    '10001010',
                                    '10001011',
                                    '10001012',
                                    '10001013',
                                    '10001014',
                                    '10001015',
                                    '10001016',
                                    '10001017']})

    def test_subent_query(self):
        self.assertEqual(
            self.dbMgr.query(
                SUBENT=10001015), {
                '10001': [
                    '10001001', '10001015']})

    def test_author_query(self):
        self.assertEqual(
            self.dbMgr.query(
                author="Panitkin"), {
                '40121': [
                    '40121001', '40121002'], '40177': [
                    '40177001', '40177002', '40177003'], '40431': [
                        '40431001', '40431002'], '41335': [
                            '41335001', '41335002']})

    def test_getitem_entry(self):
        self.assertEqual(str(self.dbMgr['E0783']), str(
            self.dbMgr.retrieve(ENTRY='E0783')))  # NEWENTRYANSWER )

    def test_getitem_subent(self):
        # , { 'E0783':[ NEWENTRYANSWER[ 'E0783' ][0], NEWENTRYANSWER[ 'E0783' ][1] ] } )
        self.assertEqual(str(self.dbMgr['E0783002']),
                         str(self.dbMgr.retrieve(SUBENT='E0783002')))

    def test_entry_retrieve(self):
        self.assertEqual(
            self.dbMgr.retrieve(
                ENTRY='E0783',
                rawEntry=True),
            NEWENTRYANSWER)

    def test_subent_retrieve(self):
        #open( 'a', mode='w' ).write( str( self.dbMgr.retrieve( SUBENT = 'E0783002' )[ 'E0783' ][0]) )
        #open( 'b', mode='w' ).write( str( NEWENTRYANSWER[ 'E0783' ][0] ) )
        self.assertEqual(self.dbMgr.retrieve(SUBENT='E0783002', rawEntry=True), {
                         'E0783': [NEWENTRYANSWER['E0783'][0], NEWENTRYANSWER['E0783'][1]]})

    def test_targ_reaction_cs_quant_query(self):
        self.assertEqual(self.dbMgr.query(target="PU-239", reaction="N,2N", quantity="CS"), {
            '13787': ['13787001', '13787002'],
            '14129': ['14129001', '14129002'],
            '21971': ['21971001', '21971003'],
            '20795': ['20795001', '20795014', '20795015'],
            '13883': ['13883001', '13883002']})

    def test_targ_reaction_da_quant_query(self):
        self.assertEqual(self.dbMgr.query(target='H-1', reaction='N,EL', quantity='DA'), {
            '10036': ['10036001', '10036002'],
            '10135': ['10135001', '10135007', '10135008'],
            '10149': ['10149001', '10149002'],
            '10187': ['10187001', '10187002'],
            '10241': ['10241001', '10241002'],
            '10275': ['10275001', '10275002'],
            '10315': ['10315001', '10315002'],
            '10316': ['10316001', '10316002', '10316003', '10316005'],
            '10355': ['10355001', '10355002', '10355003'],
            '10592': ['10592001', '10592002'],
            '10804': ['10804001', '10804002'],
            '10862': ['10862001', '10862002'],
            '10892': ['10892001', '10892002'],
            '10903': ['10903001', '10903002'],
            '11036': ['11036001', '11036002'],
            '11042': ['11042001', '11042002', '11042003'],
            '11055': ['11055001', '11055002', '11055003'],
            '11066': ['11066001', '11066002'],
            '11069': ['11069001', '11069002', '11069003'],
            '11072': ['11072001', '11072002', '11072003'],
            '11078': ['11078001', '11078002'],
            '11079': ['11079001', '11079002'],
            '11083': ['11083001', '11083002'],
            '11084': ['11084001', '11084002'],
            '11090': ['11090001', '11090002'],
            '11096': ['11096001', '11096002', '11096003'],
            '11109': ['11109001', '11109002'],
            '11117': ['11117001', '11117002'],
            '11123': ['11123001', '11123002', '11123003'],
            '11124': ['11124001', '11124002'],
            '11128': ['11128001', '11128002', '11128003'],
            '11129': ['11129001', '11129002'],
            '11131': ['11131001', '11131002'],
            '11167': ['11167001', '11167002', '11167003', '11167004'],
            '12643': ['12643001', '12643002'],
            '12656': ['12656001', '12656002', '12656003'],
            '12780': ['12780001', '12780002'],
            '12884': ['12884001', '12884003', '12884004'],
            '12909': ['12909001', '12909002'],
            '12917': ['12917001', '12917002'],
            '13150': ['13150001', '13150002', '13150003', '13150004'],
            '13623': ['13623001', '13623002'],
            '13782': ['13782001', '13782002', '13782003'],
            '13793': ['13793001', '13793002'],
            '13795': ['13795001', '13795002'],
            '13986': ['13986001', '13986002'],
            '14017': ['14017001', '14017002'],
            '14160': ['14160001', '14160002'],
            '20287': ['20287001', '20287002', '20287003'],
            '20296': ['20296001', '20296003', '20296004', '20296005', '20296007', '20296008', '20296009'],
            '20319': ['20319001', '20319002'],
            '20360': ['20360001', '20360002', '20360003'],
            '20389': ['20389001', '20389002', '20389003'],
            '20404': ['20404001', '20404002'],
            '20778': ['20778001', '20778002'],
            '20964': ['20964001', '20964002', '20964003', '20964004', '20964005', '20964006', '20964007', '20964008', '20964009', '20964010', '20964011', '20964012', '20964013', '20964014', '20964015', '20964016', '20964017', '20964018', '20964019', '20964020', '20964021', '20964022', '20964023', '20964024', '20964025', '20964026', '20964027', '20964028'],
            '21223': ['21223001', '21223002', '21223003'],
            '21365': ['21365001', '21365002'],
            '21367': ['21367001', '21367002', '21367003', '21367004'],
            '21790': ['21790001', '21790002'],
            '21795': ['21795001', '21795002'],
            '21800': ['21800001', '21800002', '21800003'],
            '21815': ['21815001', '21815002', '21815003', '21815004'],
            '21852': ['21852001', '21852002'],
            '21985': ['21985001', '21985003'],
            '21993': ['21993001', '21993002'],
            '22207': ['22207001', '22207002'],
            '22223': ['22223001', '22223002'],
            '22225': ['22225001', '22225002'],
            '22277': ['22277001', '22277002'],
            '22542': ['22542001', '22542002', '22542003'],
            '22668': ['22668001', '22668002', '22668003'],
            '22831': ['22831001', '22831036'],
            '22886': ['22886001', '22886002', '22886003'],
            '22914': ['22914001', '22914002'],
            '22949': ['22949001', '22949005'],
            '30078': ['30078001', '30078002'],
            '30162': ['30162001', '30162002', '30162003'],
            '30327': ['30327001', '30327002'],
            '30340': ['30340001', '30340003'],
            '30679': ['30679001', '30679002', '30679003', '30679004'],
            '31048': ['31048001', '31048002'],
            '41202': ['41202001', '41202002'],
            '41206': ['41206001', '41206002'],
            '41207': ['41207001', '41207002'],
            '41209': ['41209001', '41209002'],
            '41224': ['41224001', '41224002', '41224003']\
            #           u'41530': [u'41530001', u'41530002']\
        })

    def test_targ_reaction_pol_quant_query(self):
        self.maxDiff = None
        self.assertEqual(self.dbMgr.query(target='H-1', reaction='D,EL', quantity='POL/DA'), {\
            #            u'41530': [u'41530001', u'41530002'],\
            'C0606': ['C0606001', 'C0606005'],\
            'C0801': ['C0801001', 'C0801007', 'C0801008', 'C0801009', 'C0801010'],\
            'C1236': ['C1236001', 'C1236002', 'C1236003', 'C1236004', 'C1236005', 'C1236006'],\
            'C1285': ['C1285001', 'C1285002', 'C1285003', 'C1285004', 'C1285005'],\
            'C1560': ['C1560001', 'C1560002', 'C1560003', 'C1560004', 'C1560005'],\
            'D0480': ['D0480001', 'D0480003', 'D0480004', 'D0480005', 'D0480006'],\
            'E0783': ['E0783001', 'E0783002'],\
            'E0811': ['E0811001', 'E0811004', 'E0811005', 'E0811006', 'E0811007', 'E0811008', 'E0811009', 'E0811010'],\
            'E0839': ['E0839001', 'E0839003', 'E0839004', 'E0839005', 'E0839006'],\
            'E1627': ['E1627001', 'E1627002', 'E1627003', 'E1627004', 'E1627005'],\
            'E1723': ['E1723001', 'E1723003', 'E1723004', 'E1723005', 'E1723006'],\
            'E1772': ['E1772001', 'E1772005', 'E1772006', 'E1772007', 'E1772008', 'E1772009', 'E1772010', 'E1772011', 'E1772012', 'E1772013', 'E1772014', 'E1772015', 'E1772016', 'E1772017', 'E1772018', 'E1772019', 'E1772020', 'E1772021', 'E1772022', 'E1772023', 'E1772024'],\
            'E1907': ['E1907001', 'E1907002', 'E1907003', 'E1907007', 'E1907008', 'E1907009', 'E1907010', 'E1907011', 'E1907012', 'E1907013', 'E1907014'],\
            'E2008': ['E2008001', 'E2008002', 'E2008003', 'E2008004', 'E2008005', 'E2008006', 'E2008007', 'E2008008', 'E2008009'],\
            'E2052': ['E2052001', 'E2052002', 'E2052003', 'E2052004', 'E2052005', 'E2052006', 'E2052007', 'E2052008', 'E2052009'],\
            'E2159': ['E2159001', 'E2159003'],\
            'E2346': ['E2346001', 'E2346002', 'E2346003', 'E2346004', 'E2346005'],\
            'O1434': ['O1434001', 'O1434002', 'O1434003', 'O1434004'],\
            'O1664': ['O1664001', 'O1664002', 'O1664003', 'O1664004'],\
            'O1732': ['O1732001', 'O1732004'],\
            'O1974': ['O1974001', 'O1974002']
        })


if __name__ == "__main__":
    try:
        import xmlrunner
#        unittest.TestLoader().loadTestsFromTestCase( TestX4DBManagerPlainFS )
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-results'))
    except ImportError:
        unittest.main()
