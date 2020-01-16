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

import os, sys, unittest

# Set up the paths to x4i & friends
from x4i3 import exfor_manager, testDBPath, testIndexFileName

ENTRYANSWER = {'E0783': ['SUBENT        E0783001     881027\nBIB                 10         18\nTITLE       ACCELERATION OF PROTONS AND DEUTERONS POLARIZED IN\n            THE HORIZONTAL PLANEBY THE RCNP CYCLOTRON\nAUTHOR     (K.HATANAKA,N.MATSUOKA,H.SAKAI,T.SAITO,H.TAMURA,\n           K.HOSONO,M.KONDO,K.IMAI,H,SHIMIZU,K.NISHIMURA)\nINSTITUTE  (2JPNOSA) RESEARCH CENTER FOR NUCLEAR PHYSICS, OSAKA\n            UNIV.\n           (2JPNKTO)\nREFERENCE  (J,NIM,217,397,83)\nFACILITY   (CYCLO,2JPNOSA)\nINC-SOURCE  BEAM-INTENSITY IS 0.5NA\n            BEAM-POLARIZATION IS NOT GIVEN\n            ION-SOURCE=AN ATOMIC BEAM TYPE ION SOURCE WITH A\n            WIEN FILTER\nSAMPLE      TARGET IS NOT POLARIZED\n            TARGET IS NOT ALIGNED\nPART-DET   (D)\nSTATUS     (CURVE) DATA TAKEN FROM GRAPH\nHISTORY    (881027T) CONVERTED FROM NRDF DATA NO. D783\nENDBIB              18\nCOMMON               2          3\nEN         E-EXC\nMEV        MEV\n56.        0.0\nENDCOMMON            3\nENDSUBENT           25\n', 'SUBENT        E0783002     881027\nBIB                  2          2\nREACTION   (1-H-1(D,EL)1-H-1,PAR,POL/DA,,ANA)\nFLAG       (1.) DATA ERROR IS SMALLER THAN DATA POINT\nENDBIB               2\nNOCOMMON             0          0\nDATA                 4         24\nANG-CM     DATA       DATA-ERR   FLAG\nADEG       NO-DIM     NO-DIM     NO-DIM\n     30.712 -2.211E-03                    1.\n     38.727 -5.861E-03  0.821E-02\n     46.135  1.022E-02                    1.\n     55.814  4.098E-02                    1.\n     64.866  7.998E-02                    1.\n     69.415  1.126E-01                    1.\n     74.316  1.633E-01  0.147E-01\n     79.924  2.517E-01  0.115E-01\n     84.442  2.663E-01  0.131E-01\n     89.661  3.153E-01  0.821E-02\n     94.181  3.315E-01  0.164E-01\n     99.114  4.003E-01  0.115E-01\n    104.318  4.411E-01  0.131E-01\n    109.841  4.802E-01  0.132E-01\n    115.135  3.880E-01  0.132E-01\n    120.355  2.531E-01  0.131E-01\n    125.595 -5.416E-02  0.214E-01\n    129.340 -2.990E-01  0.197E-01\n    134.447 -3.140E-01  0.180E-01\n    139.629 -1.024E-01  0.197E-01\n    145.538 -2.551E-02  0.148E-01\n    150.255  1.040E-01  0.246E-01\n    155.357  8.570E-02  0.246E-01\n    160.562  1.265E-01  0.197E-01\nENDDATA             26\nENDSUBENT           33\n']}
NEWENTRYANSWER = { 'E0783':[ '''SUBENT        E0783001   20040622              20050926       0000
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
''' ] }


class TestX4DBManager( unittest.TestCase ):
    def setUp( self ):
        self.maxDiff=None
        self.dbMgr = exfor_manager.X4DBManagerPlainFS( datapath=testDBPath, database=testIndexFileName ) 
    def test_fixkey( self ):
        self.assertEqual( self.dbMgr.__fixkey__( 10001 ), '10001' )
        self.assertEqual( self.dbMgr.__fixkey__( 10001015 ), '10001015' )
        self.assertEqual( self.dbMgr.__fixkey__( '10001' ), '10001' )
        self.assertEqual( self.dbMgr.__fixkey__( '10001015' ), '10001015' )
        self.assertRaises( KeyError, self.dbMgr.__fixkey__, '1000101' )
    def test_entry_query( self ):
        self.assertEqual( self.dbMgr.query( ENTRY = 10001 ), { '10001':[ '10001001', '10001002', '10001003', '10001004', '10001005', '10001006', '10001007', '10001008', '10001009', '10001010', '10001011', '10001012', '10001013', '10001014', '10001015', '10001016', '10001017' ] } )
    def test_subent_query( self ):
        self.assertEqual( self.dbMgr.query( SUBENT = 10001015 ), { '10001':[ '10001001', '10001015' ] } )
    def test_author_query( self ):
        self.assertEqual( self.dbMgr.query( author = "Panitkin" ), { '40121':[ '40121001', '40121002' ], '40177':[ '40177001', '40177002', '40177003' ], '40431':[ '40431001', '40431002' ], '41335':[ '41335001', '41335002' ] } )
    def test_getitem_entry( self ):
        self.assertEqual( str(self.dbMgr[ 'E0783' ]), str(self.dbMgr.retrieve( ENTRY='E0783' )) ) #NEWENTRYANSWER )
    def test_getitem_subent( self ):
        self.assertEqual( str(self.dbMgr[ 'E0783002' ]), str(self.dbMgr.retrieve( SUBENT='E0783002' ) ) ) #, { 'E0783':[ NEWENTRYANSWER[ 'E0783' ][0], NEWENTRYANSWER[ 'E0783' ][1] ] } )   
    def test_entry_retrieve( self ):
        self.assertEqual( self.dbMgr.retrieve( ENTRY = 'E0783', rawEntry=True ), NEWENTRYANSWER )
    def test_subent_retrieve( self ):
        #open( 'a', mode='w' ).write( str( self.dbMgr.retrieve( SUBENT = 'E0783002' )[ 'E0783' ][0]) )
        #open( 'b', mode='w' ).write( str( NEWENTRYANSWER[ 'E0783' ][0] ) )
        self.assertEqual( self.dbMgr.retrieve( SUBENT = 'E0783002', rawEntry=True ), { 'E0783':[ NEWENTRYANSWER[ 'E0783' ][0], NEWENTRYANSWER[ 'E0783' ][1] ] } )
    def test_targ_reaction_cs_quant_query( self ):
        self.assertEqual( self.dbMgr.query( target = "PU-239", reaction = "N,2N", quantity = "CS" ), {\
            u'13787': [u'13787001', u'13787002'], \
            u'14129': [u'14129001', u'14129002'], \
            u'21971': [u'21971001', u'21971003'], \
            u'20795': [u'20795001', u'20795014', u'20795015'], \
            u'13883': [u'13883001', u'13883002']} ) 
    def test_targ_reaction_da_quant_query( self ):
        self.assertEqual( self.dbMgr.query( target = 'H-1', reaction = 'N,EL', quantity = 'DA' ), {\
            u'10036': [u'10036001', u'10036002'],  \
            u'10135': [u'10135001', u'10135007', u'10135008'],\
            u'10149': [u'10149001', u'10149002'],\
            u'10187': [u'10187001', u'10187002'],\
            u'10241': [u'10241001', u'10241002'],\
            u'10275': [u'10275001', u'10275002'],\
            u'10315': [u'10315001', u'10315002'],\
            u'10316': [u'10316001', u'10316002', u'10316003', u'10316005'],\
            u'10355': [u'10355001', u'10355002', u'10355003'],\
            u'10592': [u'10592001', u'10592002'],\
            u'10804': [u'10804001', u'10804002'],\
            u'10862': [u'10862001', u'10862002'],\
            u'10892': [u'10892001', u'10892002'],\
            u'10903': [u'10903001', u'10903002'],\
            u'11036': [u'11036001', u'11036002'],\
            u'11042': [u'11042001', u'11042002', u'11042003'],\
            u'11055': [u'11055001', u'11055002', u'11055003'],\
            u'11066': [u'11066001', u'11066002'],\
            u'11069': [u'11069001', u'11069002', u'11069003'],\
            u'11072': [u'11072001', u'11072002', u'11072003'],\
            u'11078': [u'11078001', u'11078002'],\
            u'11079': [u'11079001', u'11079002'],\
            u'11083': [u'11083001', u'11083002'],\
            u'11084': [u'11084001', u'11084002'],\
            u'11090': [u'11090001', u'11090002'],\
            u'11096': [u'11096001', u'11096002', u'11096003'],\
            u'11109': [u'11109001', u'11109002'],\
            u'11117': [u'11117001', u'11117002'],\
            u'11123': [u'11123001', u'11123002', u'11123003'],\
            u'11124': [u'11124001', u'11124002'],\
            u'11128': [u'11128001', u'11128002', u'11128003'],\
            u'11129': [u'11129001', u'11129002'],\
            u'11131': [u'11131001', u'11131002'],\
            u'11167': [u'11167001', u'11167002', u'11167003', u'11167004'],\
            u'12643': [u'12643001', u'12643002'],\
            u'12656': [u'12656001', u'12656002', u'12656003'],\
            u'12780': [u'12780001', u'12780002'],\
            u'12884': [u'12884001', u'12884003', u'12884004'],\
            u'12909': [u'12909001', u'12909002'],\
            u'12917': [u'12917001', u'12917002'],\
            u'13150': [u'13150001', u'13150002', u'13150003', u'13150004'],\
            u'13623': [u'13623001', u'13623002'],\
            u'13782': [u'13782001', u'13782002', u'13782003'],\
            u'13793': [u'13793001', u'13793002'],\
            u'13795': [u'13795001', u'13795002'],\
            u'13986': [u'13986001', u'13986002'],\
            u'14017': [u'14017001', u'14017002'],\
            u'14160': [u'14160001', u'14160002'],\
            u'20287': [u'20287001', u'20287002', u'20287003'],\
            u'20296': [u'20296001',u'20296003', u'20296004',u'20296005',u'20296007',u'20296008', u'20296009'],\
            u'20319': [u'20319001', u'20319002'],\
            u'20360': [u'20360001', u'20360002', u'20360003'],\
            u'20389': [u'20389001', u'20389002', u'20389003'],\
            u'20404': [u'20404001', u'20404002'],\
            u'20778': [u'20778001', u'20778002'],\
            u'20964': [u'20964001',u'20964002',u'20964003',u'20964004',u'20964005',u'20964006',u'20964007',u'20964008',u'20964009',u'20964010',u'20964011',u'20964012',u'20964013',u'20964014',u'20964015',u'20964016',u'20964017',u'20964018',u'20964019',u'20964020',u'20964021',u'20964022',u'20964023',u'20964024',u'20964025',u'20964026',u'20964027',u'20964028'],\
           u'21223': [u'21223001', u'21223002', u'21223003'],\
           u'21365': [u'21365001', u'21365002'],\
           u'21367': [u'21367001', u'21367002', u'21367003', u'21367004'],\
           u'21790': [u'21790001', u'21790002'],\
           u'21795': [u'21795001', u'21795002'],\
           u'21800': [u'21800001', u'21800002', u'21800003'],\
           u'21815': [u'21815001', u'21815002', u'21815003', u'21815004'],\
           u'21852': [u'21852001', u'21852002'],\
           u'21985': [u'21985001', u'21985003'],\
           u'21993': [u'21993001', u'21993002'],\
           u'22207': [u'22207001', u'22207002'],\
           u'22223': [u'22223001', u'22223002'],\
           u'22225': [u'22225001', u'22225002'],\
           u'22277': [u'22277001', u'22277002'],\
           u'22542': [u'22542001', u'22542002', u'22542003'],\
           u'22668': [u'22668001', u'22668002', u'22668003'],\
           u'22831': [u'22831001', u'22831036'],\
           u'22886': [u'22886001', u'22886002', u'22886003'],\
           u'22914': [u'22914001', u'22914002'],\
           u'22949': [u'22949001', u'22949005'],\
           u'30078': [u'30078001', u'30078002'],\
           u'30162': [u'30162001', u'30162002', u'30162003'],\
           u'30327': [u'30327001', u'30327002'],\
           u'30340': [u'30340001', u'30340003'],\
           u'30679': [u'30679001', u'30679002', u'30679003', u'30679004'],\
           u'31048': [u'31048001', u'31048002'],\
           u'41202': [u'41202001', u'41202002'],\
           u'41206': [u'41206001', u'41206002'],\
           u'41207': [u'41207001', u'41207002'],\
           u'41209': [u'41209001', u'41209002'],\
           u'41224': [u'41224001', u'41224002', u'41224003']\
#           u'41530': [u'41530001', u'41530002']\
           } ) 
    def test_targ_reaction_pol_quant_query( self ):
        self.maxDiff = None
        self.assertEqual( self.dbMgr.query( target = 'H-1', reaction = 'D,EL', quantity = 'POL/DA' ), {\
#            u'41530': [u'41530001', u'41530002'],\
            u'C0606': [u'C0606001', u'C0606005'],\
            u'C0801': [u'C0801001', u'C0801007', u'C0801008', u'C0801009', u'C0801010'],\
            u'C1236': [u'C1236001',u'C1236002',u'C1236003',u'C1236004',u'C1236005',u'C1236006'],\
            u'C1285': [u'C1285001', u'C1285002', u'C1285003', u'C1285004', u'C1285005'],\
            u'C1560': [u'C1560001', u'C1560002', u'C1560003', u'C1560004', u'C1560005'],\
            u'D0480': [u'D0480001', u'D0480003', u'D0480004', u'D0480005', u'D0480006'],\
            u'E0783': [u'E0783001', u'E0783002'],\
            u'E0811': [u'E0811001',u'E0811004',u'E0811005',u'E0811006',u'E0811007',u'E0811008',u'E0811009',u'E0811010'],\
            u'E0839': [u'E0839001', u'E0839003', u'E0839004', u'E0839005', u'E0839006'],\
            u'E1627': [u'E1627001', u'E1627002', u'E1627003', u'E1627004', u'E1627005'],\
            u'E1723': [u'E1723001', u'E1723003', u'E1723004', u'E1723005', u'E1723006'],\
            u'E1772': [u'E1772001',u'E1772005',u'E1772006',u'E1772007',u'E1772008',u'E1772009',u'E1772010',u'E1772011',u'E1772012',u'E1772013',u'E1772014',u'E1772015',u'E1772016',u'E1772017',u'E1772018',u'E1772019',u'E1772020',u'E1772021',u'E1772022',u'E1772023',u'E1772024'],\
            u'E1907': [u'E1907001',u'E1907002',u'E1907003',u'E1907007',u'E1907008',u'E1907009',u'E1907010',u'E1907011',u'E1907012',u'E1907013',u'E1907014'],\
            u'E2008': [u'E2008001',u'E2008002',u'E2008003',u'E2008004',u'E2008005',u'E2008006',u'E2008007',u'E2008008',u'E2008009'],\
            u'E2052': [u'E2052001',u'E2052002',u'E2052003',u'E2052004',u'E2052005',u'E2052006',u'E2052007',u'E2052008',u'E2052009'],\
            u'E2159': [u'E2159001', u'E2159003'],\
            u'E2346': [u'E2346001', u'E2346002', u'E2346003', u'E2346004', u'E2346005'],\
            u'O1434': [u'O1434001', u'O1434002', u'O1434003', u'O1434004'],\
            u'O1664': [u'O1664001', u'O1664002', u'O1664003', u'O1664004'],\
            u'O1732': [u'O1732001', u'O1732004'],\
            u'O1974': [u'O1974001', u'O1974002']
        } )

if __name__=="__main__": 
    try:
        import xmlrunner
#        unittest.TestLoader().loadTestsFromTestCase( TestX4DBManagerPlainFS )
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-results'))
    except ImportError:
        unittest.main()


