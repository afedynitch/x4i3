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
from x4i3 import exfor_reactions
from x4i3 import exfor_exceptions
from x4i3 import exfor_field
from x4i3 import exfor_particle
from x4i3 import exfor_grammers


class TestX4Nucleus(unittest.TestCase):
    def test_za(self):
        za = exfor_reactions.X4Nucleus("94-PU-240")
        self.assertEqual(str(za), '240Pu')
        self.assertEqual(za.asList(), ['94', 'PU', '240'])
        self.assertEqual(repr(za), '94-PU-240')
        self.assertEqual(za.endlZAStyle(), 'za094240')
        self.assertEqual(za.exforStyle(), '94-PU-240')
        self.assertEqual(za.prettyStyle(), '240Pu')
        za = exfor_reactions.X4Nucleus("94-Pu-240")
        self.assertEqual(str(za), '240Pu')
        self.assertEqual(za.asList(), ['94', 'PU', '240'])
        self.assertEqual(repr(za), '94-PU-240')
        self.assertEqual(za.endlZAStyle(), 'za094240')
        self.assertEqual(za.exforStyle(), '94-PU-240')
        self.assertEqual(za.prettyStyle(), '240Pu')
        za = exfor_reactions.X4Nucleus("94-Pu-240-")
        self.assertEqual(str(za), '240Pu')
        self.assertEqual(za.asList(), ['94', 'PU', '240'])
        self.assertEqual(repr(za), '94-PU-240')
        self.assertEqual(za.endlZAStyle(), 'za094240')
        self.assertEqual(za.exforStyle(), '94-PU-240')
        self.assertEqual(za.prettyStyle(), '240Pu')

    def test_isomers(self):
        za = exfor_reactions.X4Isomer("94-PU-240-M")
        self.assertEqual(str(za), '240mPu')
        self.assertEqual(repr(za), '94-PU-240-M')
        self.assertEqual(za.asList(), ['94', 'PU', '240', '-', 'M'])
        self.assertEqual(za.endlZAStyle(), 'za094240m')
        self.assertEqual(za.exforStyle(), '94-PU-240-M')
        self.assertEqual(za.prettyStyle(), '240mPu')
        za = exfor_reactions.X4Isomer("94-Pu-240-M2")
        self.assertEqual(str(za), '240m2Pu')
        self.assertEqual(repr(za), '94-PU-240-M2')
        self.assertEqual(za.asList(), ['94', 'PU', '240', '-', 'M', '2'])
        self.assertEqual(za.endlZAStyle(), 'za094240m2')
        self.assertEqual(za.exforStyle(), '94-PU-240-M2')
        self.assertEqual(za.prettyStyle(), '240m2Pu')

    def test_gs_isomer_sum(self):
        self.assertRaises(
            exfor_exceptions.IsomerMathParsingError,
            lambda x: exfor_reactions.X4Isomer(x),
            "94-Pu-240-G+M")
        self.assertRaises(
            exfor_exceptions.IsomerMathParsingError,
            lambda x: exfor_reactions.X4Isomer(x),
            "94-Pu-240-M1+M2")


class TestX4Particle(unittest.TestCase):
    def test_pi(self):
        self.assertEqual(str(exfor_particle.X4Particle("PIP")), "pi+")

    def test_n(self):
        self.assertEqual(str(exfor_particle.X4Particle("N")), "n")

    def test_a(self):
        self.assertEqual(str(exfor_particle.X4Particle("A")), "alpha")

    def test_he3(self):
        self.assertEqual(str(exfor_particle.X4Particle("HE3")), "He3")
#    def test_4n( self ):
#        self.assertEqual( str( exfor_particle.X4Particle( exfor_grammers.x4particle.parseString( '4N' ) ) ), '4n' )
#    def test_3he3( self ):
#        self.assertEqual( str( exfor_particle.X4Particle( exfor_grammers.x4particle.parseString( ) ) ),  )


class TestX4ChemicalCompound(unittest.TestCase):
    def test(self):
        self.assertEqual(str(exfor_particle.X4ChemicalCompound(
            "19-K-CMP")), 'Potassium compound')
        self.assertEqual(exfor_particle.X4ChemicalCompound("19-K-CMP").Z, 19)


class TextX4Process(unittest.TestCase):
    def test_n2n(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-240(N,2n)")), '240Pu(n,2n)239Pu')

    def test_nnprime(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-240(N,N)94-PU-240")), '240Pu(n,n)240Pu')

    def test_ntot(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-240(N,TOT)")), '240Pu(n,Total)')

    def test_nf(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-240(N,F)")), '240Pu(n,Fission)')

    def test_spontaneous_fission(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-240(0,F)")), '240Pu(None,Fission)')

    def test_2p4n(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-240(P,2p+4n)")), '240Pu(p,2p+4n)235Np')

    def test_heavy_ion(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-240(94-PU-240,X)")), '240Pu(240Pu,Unspecified)')

    def test_spallation(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-240(P,A+6-C-14+4N)")), '240Pu(p,alpha+14C+4n)219Fr')

    def test_kitchen_sink(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-240(P,A+6-C-14+4N+X)")), '240Pu(p,alpha+14C+4n+Unspecified)')

    def test_isomer_target(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-240-M(N,2n)")), '240mPu(n,2n)239Pu')

    def test_simple_but_important(self):
        self.assertEqual(str(exfor_reactions.X4Process(
            "94-PU-239(N,2N)94-PU-238")), '239Pu(n,2n)238Pu')

    def test_chemical_target(self):
        # print
        #print exfor_grammers.x4chemical_compound
        # print
        #print exfor_grammers.x4target
        # print
        #print exfor_grammers.Group(exfor_grammers.x4nucleus)
        # print
        #print exfor_grammers.x4target.parseString( "19-K-CMP" )
        # print
        self.assertEqual(str(exfor_reactions.X4Process(
            "19-K-CMP(N,TOT)")), 'Potassium compound(n,Total)')
        self.assertEqual(
            repr(
                exfor_reactions.X4Process("19-K-CMP(N,TOT)")),
            "19-K-CMP(N,TOT)")


class TestX4Reaction(unittest.TestCase):
    def test_simple_cs(self):
        self.assertEqual(str(exfor_reactions.X4Reaction(
            "(94-PU-239(N,F),,SIG)")), 'Cross section for 239Pu(n,Fission)')

    def test_hard_cs(self):
        self.assertEqual(str(exfor_reactions.X4Reaction(
            "(94-PU-239(P,A+6-C-14+4N),,SIG)")), 'Cross section for 239Pu(p,alpha+14C+4n)218Fr')

    def test_maxwellian_ave_cs(self):
        self.assertEqual(str(exfor_reactions.X4Reaction("(94-PU-239(N,ABS),,SIG,,MXW)")),
                         'Maxwellian average Cross section for 239Pu(n,Absorption)')

    def test_what_the_heck_is_this(self):
        self.assertEqual(str(exfor_reactions.X4Reaction("(92-U-238-M(0,F),TER,AKE,LCP)")),
                         'Avg. kin.energy light chg. part., ternary fiss. for 238mU(None,Fission)')

    def test_resonance_energy(self):
        self.assertEqual(str(exfor_reactions.X4Reaction(
            "(94-PU-240(N,0),,EN)")), '.Resonance energy for 240Pu(n,None)')

    def test_analyzing_power(self):
        self.assertEqual(str(exfor_reactions.X4Reaction("(1-H-1(D,EL)1-H-1,SL,POL/DA,,ANA)")),
                         'Vector analyzing power, A(y), for incident beam Spin-polarization probability d/dA for 1H(d,Elastic)1H')


class TestX4ReactionCombination(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(
            str(
                exfor_reactions.X4ReactionCombination("((92-U-235(N,G)92-U-236,,SIG)+(92-U-235(N,F),,SIG))")),
            '(( Cross section for 235U(n,gamma)236U )+( Cross section for 235U(n,Fission) ))')

    def test_ratio(self):
        self.assertEqual(
            str(
                exfor_reactions.X4ReactionCombination("((92-U-234(N,F),,SIG)/(92-U-235(N,F),,SIG))")),
            '(( Cross section for 234U(n,Fission) )/( Cross section for 235U(n,Fission) ))')

    def test_tautology(self):
        self.assertEqual(str(exfor_reactions.X4ReactionCombination("((19-K-CMP(N,TOT),,SIG)=(17-CL-CMP(N,TOT),,SIG))")),
                         '(( Cross section for Potassium compound(n,Total) )=( Cross section for Chlorine compound(n,Total) ))')

    def test_doubleslash(self):
        self.assertEqual(str(exfor_reactions.X4ReactionCombination("((98-CF-252(0,F),PR,DE,N)//(92-U-235(N,F),PR,DE,N,MXW))")),
                         '(( Energy spectrum of prompt fission neutrons for 252Cf(None,Fission) )//( Maxwellian average Energy spectrum of outgoing particles for 235U(n,Fission) ))')

    def test_pathological(self):
        self.assertEqual(str(exfor_reactions.X4ReactionCombination("(((94-PU-239(N,F),,SIG)-(92-U-238-M(0,F),TER,AKE,LCP))/(94-PU-239(N,ABS),,SIG,,MXW))")),
                         '((( Cross section for 239Pu(n,Fission) )-( Avg. kin.energy light chg. part., ternary fiss. for 238mU(None,Fission) ))/( Maxwellian average Cross section for 239Pu(n,Absorption) ))')

    def test_sum_with_isomer(self):
        self.assertEqual(
            str(
                exfor_reactions.X4ReactionCombination("((79-AU-197(N,2N)79-AU-196-G,,SIG)+(79-AU-197(N,2N)79-AU-196-M1,,SIG))")),
            '(( Cross section for 197Au(n,2n)196m0Au )+( Cross section for 197Au(n,2n)196mAu ))')

    def test_you_are_friggen_kidding(self):
        self.assertEqual(str(exfor_reactions.X4ReactionCombination("((79-AU-197(N,2N)79-AU-196-M2,,SIG)/(79-AU-197(N,2N)79-AU-196-G+M1,,SIG))")),
                         '(( Cross section for 197Au(n,2n)196m2Au )/( (( Cross section for 197Au(n,2n)196m0Au )+( Cross section for 197Au(n,2n)196mAu )) ))')


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-results'))
    except ImportError:
        unittest.main()
        print()
        print()
