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
from x4i3 import exfor_field
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
test_common = '''COMMON               1          3\nEN         \nMEV        \n56.        \nENDCOMMON            3'''
test_entry_2 = (
    ''.join(
        open(
            __path__[0] +
            os.sep +
            '12898.x4',
            mode='r').readlines())).replace(
                '\r',
    '')


class TestX4PlainField(unittest.TestCase):

    def setUp(self):
        self.instring = '''INC-SOURCE  BEAM-INTENSITY IS 0.5NA\n            BEAM-POLARIZATION IS NOT GIVEN\n           (ATOMI) with a Wien filter'''
        self.field = exfor_field.X4PlainField(self.instring.split('\n'))

    def test_repr(self):
        self.assertEqual(repr(self.field), self.instring)

    def test_tag(self):
        self.assertEqual(self.field.tag, 'INC-SOURCE')


class TestX4PlainFieldPointer(unittest.TestCase):

    def setUp(self):
        self.instring = '''REACTION  1((30-ZN-64(N,G)30-ZN-65,,RI)/\n           (30-ZN-64(N,G)30-ZN-65,,SIG))\n          2(30-ZN-64(N,G)30-ZN-65,,RI)\n           Reduced resonance integral and ratio to thermal\n           absorption cross section'''
        self.field = exfor_field.X4PlainField(self.instring.split('\n'))

    def test_ptr(self):
        self.assertEqual(self.field.sorted_keys, ['1', '2'])

    def test_repr(self):
        #open( 'a', mode='w' ).writelines( repr( self.field ) )
        #open( 'b', mode='w' ).writelines( self.instring )
        self.assertEqual(repr(self.field), self.instring)

    def test_tag(self):
        self.assertEqual(self.field.tag, 'REACTION')


class TestX4ReactionField(unittest.TestCase):
    
    def setUp(self):
        self.instring = '''REACTION   ((30-ZN-64(N,G)30-ZN-65,,RI)/\n           (30-ZN-64(N,G)30-ZN-65,,SIG))'''
        self.field = exfor_field.X4ReactionField(self.instring.split('\n'))

    def test_repr(self):
        self.assertEqual(repr(self.field), self.instring)

    def test_str(self):
        self.assertEqual(str(
            self.field), '(( Resonance integral for 64Zn(n,gamma)65Zn )/( Cross section for 64Zn(n,gamma)65Zn ))')

    def test_tag(self):
        self.assertEqual(self.field.tag, 'REACTION')

    def test_you_gotta_be_kidding(self):
        testFieldString = '''REACTION   ((79-AU-197(N,2N)79-AU-196-M2,,SIG)/
           (79-AU-197(N,2N)79-AU-196-G+M1,,SIG))
           Isomeric ratio sigma(m2)/sigma(g.s.+ m1)'''
        testField = exfor_field.X4ReactionField(testFieldString.split('\n'))
        self.assertEqual(
            str(testField),
            '(( Cross section for 197Au(n,2n)196m2Au )/( (( Cross section for 197Au(n,2n)196m0Au )+( Cross section for 197Au(n,2n)196mAu )) ))')

    def test_no_you_really_gotta_be_kidding(self):
        testFieldString = '''REACTION   (48-CD-116(N,2N)48-CD-115-M/G,,SIG/RAT)'''
        testField = exfor_field.X4ReactionField(testFieldString.split('\n'))
        self.assertEqual(
            str(testField),
            '(( Cross section ratio for 116Cd(n,2n)115mCd )/( Cross section ratio for 116Cd(n,2n)115m0Cd ))')

    def test_please_stop(self):
        testFieldString = '''REACTION  1(40-ZR-88(N,N+P)39-Y-87-M/T,,SIG/RAT)
          2(40-ZR-88(N,N+P)39-Y-87,,SIG)'''
        testField = exfor_field.X4ReactionField(testFieldString.split('\n'))
        self.assertEqual(
            str(testField),
            '[1] (( Cross section ratio for 88Zr(n,n+p)87mY )/( Cross section ratio for 88Zr(n,n+p)87mY )); [2] Cross section for 88Zr(n,n+p)87Y')

    def test_oh_god_no(self):
        testFieldString = 'REACTION   (96-CM-248(10-NE-22,5N)106-SG-265-M1+M2,,SIG)'
        testField = exfor_field.X4ReactionField(testFieldString.split('\n'))
        self.assertEqual(
            str(testField),
            '(( Cross section for 248Cm(22Ne,5n)265mSg )+( Cross section for 248Cm(22Ne,5n)265m2Sg ))')
        
        testFieldString = '''REACTION  1(44-RU-OXI(N,THS)44-RU-OXI,BA/COH,AMP)
          2(44-RU-OXI(N,THS)44-RU-OXI,BA/COH,AMP)
          3(44-RU-OXI(N,THS)44-RU-OXI,BA/COH,AMP) Bound molecule
            coherent scattering length at zero neutron energy.'''
        testField = exfor_field.X4ReactionField(testFieldString.split('\n'))
        self.assertEqual(str(testField), '[1] Bound-atom coherent scattering amplitude for Ruthenium oxide(n,ThermalScattering)Ruthenium oxide; [2] Bound-atom coherent scattering amplitude for Ruthenium oxide(n,ThermalScattering)Ruthenium oxide; [3] Bound-atom coherent scattering amplitude for Ruthenium oxide(n,ThermalScattering)Ruthenium oxide, Bound molecule coherent scattering length at zero neutron energy.')
        
        testFieldString = '''REACTION  1(72-HF-178-M2(N,G)72-HF-179-G,,SIG)
          2(72-HF-178-M2(N,G)72-HF-179-G,,RI)
          3(72-HF-178-M2(N,G)72-HF-179-M2/G,,SIG/RAT)
          4(72-HF-178-M2(N,G)72-HF-179-M2,,SIG)
          5(72-HF-178-M2(N,G)72-HF-179-M2,,RI)'''
        testField = exfor_field.X4ReactionField(testFieldString.split('\n'))
        self.assertEqual(
            str(testField),
            '[1] Cross section for 178m2Hf(n,gamma)179m0Hf; [2] Resonance integral for 178m2Hf(n,gamma)179m0Hf; [3] (( Cross section ratio for 178m2Hf(n,gamma)179m2Hf )/( Cross section ratio for 178m2Hf(n,gamma)179m0Hf )); [4] Cross section for 178m2Hf(n,gamma)179m2Hf; [5] Resonance integral for 178m2Hf(n,gamma)179m2Hf')
        testFieldString = '''REACTION   (72-HF-178-M2(N,G)72-HF-179-G+M2,,SIG,,RES)    Indivi-
            dual resonance contribution in capture cross-section'''
        testField = exfor_field.X4ReactionField(testFieldString.split('\n'))
        self.assertEqual(
            str(testField),
            '(( Cross section for 178m2Hf(n,gamma)179m0Hf )+( Cross section for 178m2Hf(n,gamma)179m2Hf ))')
        testFieldString = '''REACTION   ((94-PU-239(N,F),,SIG)/
           (92-U-235(N,F),,SIG))'''
        testField = exfor_field.X4ReactionField(testFieldString.split('\n'))
        self.assertEqual(
            str(testField),
            '(( Cross section for 239Pu(n,Fission) )/( Cross section for 235U(n,Fission) ))')
        testFieldString = '''REACTION   ((92-U-233(N,F),,SIG)/
           (92-U-235(N,F),,SIG))'''
        testField = exfor_field.X4ReactionField(testFieldString.split('\n'))
        self.assertEqual(
            str(testField),
            '(( Cross section for 233U(n,Fission) )/( Cross section for 235U(n,Fission) ))')


class TestX4ReactionFieldPointer(unittest.TestCase):

    def setUp(self):
        self.instring = '''REACTION  1((30-ZN-64(N,G)30-ZN-65,,RI)/\n           (30-ZN-64(N,G)30-ZN-65,,SIG))\n          2(30-ZN-64(N,G)30-ZN-65,,RI)\n           Reduced resonance integral and ratio to thermal\n           absorption cross section'''
        self.field = exfor_field.X4ReactionField(self.instring.split('\n'))

    def test_repr(self):
        self.assertEqual(repr(self.field), self.instring)

    def test_str(self):
        self.assertEqual(
            str(
                self.field),
            '[1] (( Resonance integral for 64Zn(n,gamma)65Zn )/( Cross section for 64Zn(n,gamma)65Zn )); [2] Resonance integral for 64Zn(n,gamma)65Zn, Reduced resonance integral and ratio to thermal absorption cross section')

    def test_tag(self):
        self.assertEqual(self.field.tag, 'REACTION')


class TestX4TitleField(unittest.TestCase):

    def setUp(self):
        self.short_example = '''TITLE       ACCELERATION OF PROTONS AND DEUTERONS POLARIZED'''
        self.long_example = '''TITLE      MEASURED ACTIVATION CROSS SECTIONS BELOW 10 MEV FOR THE\n            51-V(N,P)51-TI AND 51-V(N,ALPHA)48-SC REACTIONS.'''

    def test_oneline(self):
        self.assertEqual(str(exfor_field.X4TitleField(self.short_example.split(
            '\n'))), 'Acceleration Of Protons And Deuterons Polarized')
        self.assertEqual(
            repr(
                exfor_field.X4TitleField(
                    self.short_example.split('\n'))),
            self.short_example)

    def test_multiline(self):
        self.assertEqual(str(exfor_field.X4TitleField(self.long_example.split(
            '\n'))), 'Measured Activation Cross Sections Below 10 Mev For The 51-V(N,P)51-Ti And 51-V(N,Alpha)48-Sc Reactions.')
        self.assertEqual(
            repr(
                exfor_field.X4TitleField(
                    self.long_example.split('\n'))),
            self.long_example)


class TestX4MonitorField(unittest.TestCase):

    def setUp(self):
        self.really_short_example = '''MONITOR    (92-U-235(N,F),,SIG)'''
        self.short_example = '''MONITOR   1(79-AU-197(N,2N)79-AU-196,,SIG)'''
        self.medium_example = '''MONITOR    (62-SM-147(N,A)60-ND-144,,SIG) Data were normalized
           over the interval 300-2500 eV to the data given
           in monitor reference'''
        self.boring_example = '''MONITOR    Reactor grade graphite samples with thickness of 7
           cm and 13 cm were useded for monitoring'''
        self.long_example = '''MONITOR    ((MONIT1)79-AU-197(N,G)79-AU-198,,RI)
           ((MONIT2)27-CO-59(N,G)27-CO-60,,RI)'''
        self.another_long_example = '''MONITOR    (22-TI-0(D,X)23-V-48,,SIG) 21 MeV
           (13-AL-27(D,X)11-NA-22,,SIG)  40 MeV
           (13-AL-27(D,X)11-NA-24,,SIG)  40 MeV'''
        self.really_long_example = '''MONITOR    ((MONIT1)79-AU-197(N,G)79-AU-198,,SIG,,MXW) Monitor in
             form of alloy of 0.134% in thin Al metal foil
           ((MONIT3)27-CO-59(N,G)27-CO-60,,SIG,,MXW) Monitor in
           form of dilute  alloy  of 0.438% in thin Al metal foil'''
        self.combo_example = '''MONITOR    ((29-CU-63(A,N+P)30-ZN-65,,TTY)+
           (29-CU-63(A,2N)31-GA-65,,TTY))'''
        self.simple_boring_example = '''MONITOR    No information'''
        self.kitchen_sink_example = '''MONITOR    ((MONIT1)(95-AM-241(N,F)42-MO-99,CUM,FY,,SPA)+
           (95-AM-241(N,F)43-TC-99-M,CUM,FY,,SPA)) USED FOR
            NORMALIZATION OF THE LIGHT-MASS PEAK, I.E. A = 91
            TO 105.
           ((MONIT2)95-AM-241(N,F)56-BA-139,CUM,FY,,SPA) USED FOR
            NORMALIZATION OF THE HEAVY-MASS PEAK, I.E. A = 131 TO
            147.'''

    def test_oneline(self):
        X = exfor_field.X4MonitorField(self.really_short_example.split('\n'))
        self.assertEqual(repr(X), self.really_short_example)
        self.assertEqual(str(X.reactions), "{' ': [((92-U-235(N,F),SIG), '', None)]}")
        self.assertEqual(str(X), "[((92-U-235(N,F),SIG), '', None)]")

    def test_oneline_pointer(self):
        X = exfor_field.X4MonitorField(self.short_example.split('\n'))
        self.assertEqual(repr(X), self.short_example)
        self.assertEqual(str(X.reactions),
                         "{'1': [((79-AU-197(N,2N)79-AU-196,SIG), '', None)]}")
        self.assertEqual(str(X), "[1] [((79-AU-197(N,2N)79-AU-196,SIG), '', None)]")

    def test_multiline(self):
        X = exfor_field.X4MonitorField(self.medium_example.split('\n'))
        self.assertEqual(repr(X), self.medium_example)
        self.assertEqual(str(
            X.reactions), "{' ': [((62-SM-147(N,A)60-ND-144,SIG), 'Data were normalized over the interval 300-2500 eV to the data given in monitor reference', None)]}")
        self.assertEqual(
            str(X),
            "[((62-SM-147(N,A)60-ND-144,SIG), 'Data were normalized over the interval 300-2500 eV to the data given in monitor reference', None)]")
        self.assertEqual(list(X.reactions.keys()), [' '])
        self.assertEqual(
            X.reactions[' '][0][1],
            'Data were normalized over the interval 300-2500 eV to the data given in monitor reference')

    def test_multiline_boring(self):
        X = exfor_field.X4MonitorField(self.boring_example.split('\n'))
        self.assertEqual(repr(X), self.boring_example)
        self.assertEqual(str(
            X.reactions), "{' ': [(None, 'Reactor grade graphite samples with thickness of 7 cm and 13 cm were useded for monitoring', None)]}")
        self.assertEqual(
            str(X),
            "[(None, 'Reactor grade graphite samples with thickness of 7 cm and 13 cm were useded for monitoring', None)]")

    def test_two_monitors(self):
        X = exfor_field.X4MonitorField(self.long_example.split('\n'))
        self.assertEqual(repr(X), self.long_example)
        self.assertEqual(str(
            X.reactions), "{' ': [((79-AU-197(N,G)79-AU-198,RI), '', 'MONIT1'), ((27-CO-59(N,G)27-CO-60,RI), '', 'MONIT2')]}")
        self.assertEqual(
            str(X),
            "[((79-AU-197(N,G)79-AU-198,RI), '', 'MONIT1'), ((27-CO-59(N,G)27-CO-60,RI), '', 'MONIT2')]")

    def test_three_monitors(self):
        X = exfor_field.X4MonitorField(self.another_long_example.split('\n'))
        self.assertEqual(repr(X), self.another_long_example)
        self.assertEqual(str(
            X.reactions), "{' ': [((22-TI-0(D,X+23-V-48),SIG), '21 MeV', None), ((13-AL-27(D,X+11-NA-22),SIG), '40 MeV', None), ((13-AL-27(D,X+11-NA-24),SIG), '40 MeV', None)]}")
        self.assertEqual(list(X.reactions.keys()), [' '])
        self.assertEqual(X.reactions[' '][0][1], '21 MeV')

    def test_two_monitors_many_lines(self):
        X = exfor_field.X4MonitorField(self.really_long_example.split('\n'))
        self.assertEqual(repr(X), self.really_long_example)
        self.assertEqual(
            str(
                X.reactions),
            "{' ': [((79-AU-197(N,G)79-AU-198,SIG,MXW), 'Monitor in form of alloy of 0.134% in thin Al metal foil', 'MONIT1'), ((27-CO-59(N,G)27-CO-60,SIG,MXW), 'Monitor in form of dilute  alloy  of 0.438% in thin Al metal foil', 'MONIT3')]}")
        self.assertEqual(
            str(X),
            "[((79-AU-197(N,G)79-AU-198,SIG,MXW), 'Monitor in form of alloy of 0.134% in thin Al metal foil', 'MONIT1'), ((27-CO-59(N,G)27-CO-60,SIG,MXW), 'Monitor in form of dilute  alloy  of 0.438% in thin Al metal foil', 'MONIT3')]")

    def test_combo(self):
        X = exfor_field.X4MonitorField(self.combo_example.split('\n'))
        self.assertEqual(
            str(X),
            "[((( (29-CU-63(A,N+P)30-ZN-65,TTY) )+( (29-CU-63(A,2N)31-GA-65,TTY) )), '', None)]")

    def test_simple_boring(self):
        X = exfor_field.X4MonitorField(self.simple_boring_example.split('\n'))
        self.assertEqual(str(X), "[(None, 'No information', None)]")

    def test_kitchen_sink(self):
        X = exfor_field.X4MonitorField(self.kitchen_sink_example.split('\n'))
        self.assertEqual(str(X), "[((( (95-AM-241(N,F+42-MO-99),CUM,FY,SPA) )+( (95-AM-241(N,F+43-TC-99-M),CUM,FY,SPA) )), 'USED FOR NORMALIZATION OF THE LIGHT-MASS PEAK, I.E. A = 91 TO 105.', 'MONIT1'), ((95-AM-241(N,F+56-BA-139),CUM,FY,SPA), 'USED FOR NORMALIZATION OF THE HEAVY-MASS PEAK, I.E. A = 131 TO 147.', 'MONIT2')]")
#        X = exfor_field.X4MonitorField( '''MONITOR    .The cross-section ratios were obtained by
#            absolute measurements in contrast to earlier work
#            (W.D.Allen,a.T.G.Ferguson proc.Phys.Soc.,70A(1957)573,
#            G.N.Smirenkin et al, Atomn.En.,13(1962)366).'''  )
#        self.assertEqual( str( X ), '')


class TestX4AuthorField(unittest.TestCase):

    def setUp(self):
        self.short_example = '''AUTHOR     (D.L.SMITH,J.W.MEADOWS,I.KANNO)'''
        self.long_example = '''AUTHOR     (K.HATANAKA,N.MATSUOKA,H.SAKAI,T.SAITO,H.TAMURA,\n           K.HOSONO,M.KONDO,K.IMAI,H.SHIMIZU,K.NISHIMURA)'''
        self.really_long_example = '''AUTHOR     (A.Budzanowski, A.Chatterjee, R.Gebel, P.Hawranek,
           R.Jahn, V.Jha, K.Kilian, S.Kliczewski, Da.Kirillov,
           Di.Kirillov, D.Kolev, M.Kravcikova, M.Lesiak, J.Lieb,
           H.Machner, A.Magiera, R.Maier, G.Martinska, S.Nedev,
           N.Piskunov, D.Prasuhn, D.Protic, J.Ritman,
           P.von Rossen, B.J.Roy, I.Sitnik, R.Siudak, R.Tsenov,
           J.Urban, G.Vankova, C.Wilkin) GEM Collaboration'''

    def test_oneline(self):
        self.assertEqual(
            repr(
                exfor_field.X4AuthorField(
                    self.short_example.split('\n'))),
            self.short_example)
        self.assertEqual(str(exfor_field.X4AuthorField(
            self.short_example.split('\n'))), 'D.L.Smith, J.W.Meadows, I.Kanno')
        self.assertEqual(
            exfor_field.X4AuthorField(
                self.short_example.split('\n')).author_family_names, [
                'Smith', 'Meadows', 'Kanno'])

    def test_multiline(self):
        self.assertEqual(
            repr(
                exfor_field.X4AuthorField(
                    self.long_example.split('\n'))),
            self.long_example)
        self.assertEqual(exfor_field.X4AuthorField(self.long_example.split('\n')).author_family_names, [
                         'Hatanaka', 'Matsuoka', 'Sakai', 'Saito', 'Tamura', 'Hosono', 'Kondo', 'Imai', 'Shimizu', 'Nishimura'])
        self.assertEqual(str(exfor_field.X4AuthorField(self.long_example.split(
            '\n'))), 'K.Hatanaka, N.Matsuoka, H.Sakai, T.Saito, H.Tamura, K.Hosono, M.Kondo, K.Imai, H.Shimizu, K.Nishimura')

    def test_really_long(self):
        self.assertEqual(
            repr(
                exfor_field.X4AuthorField(
                    self.really_long_example.split('\n'))),
            self.really_long_example)
        self.assertEqual(
            exfor_field.X4AuthorField(
                self.really_long_example.split('\n')).author_family_names,
            [
                'Budzanowski',
                'Chatterjee',
                'Gebel',
                'Hawranek',
                'Jahn',
                'Jha',
                'Kilian',
                'Kliczewski',
                'Kirillov',
                'Kirillov',
                'Kolev',
                'Kravcikova',
                'Lesiak',
                'Lieb',
                'Machner',
                'Magiera',
                'Maier',
                'Martinska',
                'Nedev',
                'Piskunov',
                'Prasuhn',
                'Protic',
                'Ritman',
                'Von Rossen',
                'Roy',
                'Sitnik',
                'Siudak',
                'Tsenov',
                'Urban',
                'Vankova',
                'Wilkin'])
        self.assertEqual(
            str(
                exfor_field.X4AuthorField(
                    self.really_long_example.split('\n'))),
            'A.Budzanowski, A.Chatterjee, R.Gebel, P.Hawranek, R.Jahn, V.Jha, K.Kilian, S.Kliczewski, Da.Kirillov, Di.Kirillov, D.Kolev, M.Kravcikova, M.Lesiak, J.Lieb, H.Machner, A.Magiera, R.Maier, G.Martinska, S.Nedev, N.Piskunov, D.Prasuhn, D.Protic, J.Ritman, P.Von Rossen, B.J.Roy, I.Sitnik, R.Siudak, R.Tsenov, J.Urban, G.Vankova, C.Wilkin')


class TestX4InstituteField(unittest.TestCase):

    def setUp(self):
        self.short_example = '''INSTITUTE  (1USAANL)'''
        self.long_example = '''INSTITUTE  (2JPNOSA) RESEARCH CENTER FOR NUCLEAR PHYSICS, OSAKA\n            UNIV.\n           (2JPNKTO)'''
        self.really_long_example = '''INSTITUTE  (3POLIFJ)
           (3INDTRM)
           (2GERJUL)
           (3POLUJK)
           (2GERBON)
           (2GERUDE)
           (4ZZZDUB)
           (3BULSOF)
           (3SLKSLK) Technical university, Kosice, Slovakia
           (1USAUSA) George Mason University, Fairfax, VA, USA
           (3SLKSLK) P.J. Safarik University, Kosice, Slovakia
           (3BULBUL) University of chemical technology and
                      Metallurgy, Sofia, Bulgaria
           (2UK UK) Department of physics and Astronomy, UCL,
                    London, UK'''
        self.yae = '''INSTITUTE  (2GERIFS,2GERKLN,1USAKTY)'''  # x4i FAILS THIS TEST AS OF 12/23/2009

    def test_oneline(self):
        self.assertEqual(
            repr(
                exfor_field.X4InstituteField(
                    self.short_example.split('\n'))),
            self.short_example)
        self.assertEqual(str(exfor_field.X4InstituteField(
            self.short_example.split('\n'))), 'Argonne National Laboratory, Argonne, IL')

    def test_multiline(self):
        self.assertEqual(
            repr(
                exfor_field.X4InstituteField(
                    self.long_example.split('\n'))),
            self.long_example)
        self.assertEqual(str(exfor_field.X4InstituteField(self.long_example.split(
            '\n'))), 'Osaka Univ., Osaka (Research Center For Nuclear Physics, Osaka Univ.); Kyoto Univ.')

    def test_really_long(self):
        self.assertEqual(
            repr(
                exfor_field.X4InstituteField(
                    self.really_long_example.split('\n'))),
            self.really_long_example)
        self.assertEqual(str(exfor_field.X4InstituteField(self.really_long_example.split('\n'))), 'Inst.Fiz.Jadr., Krakow; Bhabha Atomic Res. Centre, Trombay; Kernforschungsanlage Juelich; Krakow, Jagellonian Univ; Univ. of Bonn; 2GERUDE; Joint Inst.for Nucl.Res., Dubna; Univ.of Sofia; Slovakia (Technical University, Kosice, Slovakia); United States of America (George Mason University, Fairfax, Va, Usa); Slovakia (P.J. Safarik University, Kosice, Slovakia); Bulgaria (University Of Chemical Technology And Metallurgy, Sofia, Bulgaria); 2UK (Department Of Physics And Astronomy, Ucl, London, Uk)')


class TestX4ReferenceField(unittest.TestCase):

    def setUp(self):
        self.short_example = '''REFERENCE  (J,NIM,217,397,1983)'''
        self.long_example = '''REFERENCE  (J,ANE,11,623,8412)\n           (P,ANL-NDM-85,8406)'''
        self.really_long_example = '''REFERENCE  (J,APP/B,2,489,1971) Full information\n           (P,INR-1318,29,197104)Partial,total sigmas cfd theory\n           (P,INDC(SEC)-18,120,197108) Identical to INR-1318\n           (R,INR-1224,197009)Experim.set-up described.Full paper\n           (P,INR-1197,26,197005)Small reprt.Same info as INR-1224\n           (J,CJP,47,2849,196912) Theo. Calculation of (n,g) sigma'''
        self.tautology_example = '''REFERENCE  ((W,KOBAYASHI,73)=(R,KURRI-TR-6,1,73))\n            ANNU.REP.RES.REACTOR INST., KYOTO UNIV.\n           (P,EANDC(J)-26,39,7208) PROG.REP. FOR NP-237 AND TH-232'''
        self.another_tautology_example = '''REFERENCE  (J,NP,70,421,6508)
           ((R,JAERI-1078,6507)=(R,EANDC(J)-5S,6507))
           (W,NISHIMURA,7110)'''
        self.tautology_string = '''REFERENCE  ((R,CEA-N-1459,7108)=(R,EANDC(E)-142L,7108)=
           (R,INDC(FR)-4L,7108)) INTERNAL REPT,EXP.DESCR.,RES.PAR.
            RESONANCE PARAMETERS CODED IN ENTRY 20121.
           (W,TELLIER,7110)     DATA ON TAPES.'''
        self.ya_tautology_example = '''REFERENCE  (J,NST,31,1239,199412)  Main reference, data are given\n           ((S,JAERI-M-94-019,171,199311)=\n           (S,INDC(JPN)-169/L,171,199311))'''
        self.tricky_tautology_example = '''REFERENCE  ((R,YK-5(49),17,198211)=\n           (J,YK,1982,(5),17,198211))  Main Reference'''
        self.bathroom_sink_tautology_example = '''REFERENCE  (P,NEANDC(E)-232,(3),5,198203) Main reference,
                                        DATA ARE GIVEN.
           (P,NEANDC(E)-222,(3),3,198103)
           ((R,ANL-83-4,1983)=
           (R,NEANDC(US)-214,1983))  ANL-83-4 report.
                                     Data are given
           (P,NEANDC(E)-212,(3),10,198006)'''
        self.kitchen_sink_tautology_example = '''REFERENCE  (J,NSTS,2,(1),204,200208)  Main referene, Graphs Given
           (J,NSTS,1,683,2000)        Details of Experiment
           (J,NIM/A,446,(3),536,2000) Graphs and Experimental
                                      details
           ((S,JAERI-C-2000-005,243,19991119)=
           (S,INDC(JPN)-185/U,243,19991119)) Graphs and
                                        Experimental Details
           ((S,JAERI-C-99-002,153,19981120)=
           (S,INDC(JPN)-182/U,153,19981120)) Graphs and
                                        Experimental Details'''
        self.doi = '''REFERENCE  (J,PR/C,72,034302,2005)\n           #DOi=10.1103/PhysRevC.72.034302'''

    def test_oneline(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.short_example.split('\n'))),
            self.short_example)
        self.assertEqual(str(exfor_field.X4ReferenceField(self.short_example.split(
            '\n'))), 'Nuclear Instrum.and Methods in Physics Res. 217, 397 (1983)')

    def test_doi(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.doi.split('\n'))),
            self.doi)
        self.assertEqual(str(exfor_field.X4ReferenceField(self.doi.split('\n'))),
                         'Physical Review, Part C, Nuclear Physics 72, 034302 (2005)')

    def test_multiline(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.long_example.split('\n'))),
            self.long_example)
        self.assertEqual(str(exfor_field.X4ReferenceField(self.long_example.split(
            '\n'))), 'Annals of Nuclear Energy 11, 623 (1984); Progress report: ANL-NDM-85  (1984)')

    def test_reallylong(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.really_long_example.split('\n'))),
            self.really_long_example)
        self.assertEqual(str(exfor_field.X4ReferenceField(self.really_long_example.split(
            '\n'))), 'Acta Physica Polonica, Part B 2, 489 (1971); Progress report: INR-1318 29 (1971); Progress report: INDC(SEC)-18 120 (1971); Report other than progress report: INR-1224  (1970); Progress report: INR-1197 26 (1970); Canadian Journal of Physics 47, 2849 (1969)')

    def test_tautology(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.tautology_example.split('\n'))),
            self.tautology_example)
        self.assertEqual(str(exfor_field.X4ReferenceField(self.tautology_example.split(
            '\n'))), 'Private communication: Kobayashi  (1973); Report other than progress report: KURRI-TR-6 1 (1973); Progress report: EANDC(J)-26 39 (1972)')

    def test_another_tautology(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.another_tautology_example.split('\n'))),
            self.another_tautology_example)
        self.assertEqual(str(exfor_field.X4ReferenceField(self.another_tautology_example.split(
            '\n'))), 'Nuclear Physics 70, 421 (1965); Report other than progress report: JAERI-1078  (1965); Report other than progress report: EANDC(J)-5S  (1965); Private communication: Nishimura  (1971)')

    def test_tautology_string(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.tautology_string.split('\n'))),
            self.tautology_string)
        self.assertEqual(str(exfor_field.X4ReferenceField(self.tautology_string.split(
            '\n'))), 'Report other than progress report: CEA-N-1459  (1971); Report other than progress report: EANDC(E)-142L  (1971); Report other than progress report: INDC(FR)-4L  (1971); Private communication: Tellier  (1971)')

    def test_ya_tautology_example(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.ya_tautology_example.split('\n'))),
            self.ya_tautology_example)
        self.assertEqual(str(exfor_field.X4ReferenceField(self.ya_tautology_example.split(
            '\n'))), 'J. of Nuclear Science and Technology, Tokyo 31, 1239 (1994); Report containing conference proc.: JAERI-M-94-019 171 (1993); Report containing conference proc.: INDC(JPN)-169/L 171 (1993)')

    def test_tricky_tautology_example(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.tricky_tautology_example.split('\n'))),
            self.tricky_tautology_example)
        self.assertEqual(str(exfor_field.X4ReferenceField(self.tricky_tautology_example.split(
            '\n'))), 'Report other than progress report: YK-5(49) 17 (1982); Vop. At.Nauki i Tekhn.,Ser.Yadernye Konstanty 1982, (5), 17 (1982)')

    def test_bathroom_sink(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.bathroom_sink_tautology_example.split('\n'))),
            self.bathroom_sink_tautology_example)
        self.assertEqual(str(exfor_field.X4ReferenceField(self.bathroom_sink_tautology_example.split(
            '\n'))), 'Progress report: NEANDC(E)-232 (3), 5 (1982); Progress report: NEANDC(E)-222 (3), 3 (1981); Report other than progress report: ANL-83-4  (1983); Report other than progress report: NEANDC(US)-214  (1983); Progress report: NEANDC(E)-212 (3), 10 (1980)')

    def test_kitchen_sink(self):
        self.assertEqual(
            repr(
                exfor_field.X4ReferenceField(
                    self.kitchen_sink_tautology_example.split('\n'))),
            self.kitchen_sink_tautology_example)
        self.assertEqual(
            str(
                exfor_field.X4ReferenceField(
                    self.kitchen_sink_tautology_example.split('\n'))),
            'J.Nucl.Science and Technol.Tokyo,Supplement 2, (1), 204 (2002); J.Nucl.Science and Technol.Tokyo,Supplement 1, 683 (2000); Nucl. Instrum. Methods in Physics Res., Sect.A 446, (3), 536 (2000); Report containing conference proc.: JAERI-C-2000-005 243 (1999); Report containing conference proc.: INDC(JPN)-185/U 243 (1999); Report containing conference proc.: JAERI-C-99-002 153 (1998); Report containing conference proc.: INDC(JPN)-182/U 153 (1998)')


if __name__ == "__main__":
    #    try:
    #        import xmlrunner
    #        unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-results'))
    #    except ImportError:
    unittest.main()
    print()
    print()
