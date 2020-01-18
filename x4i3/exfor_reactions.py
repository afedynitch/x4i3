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

import sys

from .endl_Z import endl_ZSymbol
from .exfor_exceptions import (
    ReactionParsingError,
    ResidualNucleusError,
    IsomerMathParsingError)
from .exfor_utilities import x4Dictionaries
from .exfor_grammers import (
    x4process,
    x4particle,
    x4reaction,
    x4compound_expression,
    x4reactionfield,
    x4nucleus)
from .exfor_particle import (
    X4Particle,
    X4Element,
    X4Nucleus,
    X4Isomer,
    X4ChemicalCompound,
    X4VariableParticle)

if sys.version_info < (3, 0, 0):
    from .pyparsing2 import ParseException, ParseResults
else:
    from .pyparsing3 import ParseException, ParseResults

# ------------------------------------------------------
# Global data
# ------------------------------------------------------
VERBOSELEVEL = 2
x4ReactionMap = {
    'TOT': 'Total',
    'EL': 'Elastic',
    'ABS': 'Absorption',
    'INL': 'Inelastic',
    'TCC': 'TotalChargeChanging',
    'FUS': 'Fusion',
    'NON': 'Nonelastic',
    'SCT': 'Scattering',
    'F': 'Fission',
    'PAI': 'PairProduction',
    'THS': 'ThermalScattering',
    'X': 'Unspecified',
    '0': 'None'}
x4QuantityMap = x4Dictionaries['Quantities']
x4ModifierMap = x4Dictionaries['Modifiers']


class X4Process:
    """Parsed Exfor process, namely just the "target+projectile -> stuff" part of a string"""

    def __init__(self, xl, IgnoreIsomerMath=False):
        if isinstance(xl, str):
            xl = self.parse(xl)
        if not isinstance(xl, ParseResults):
            raise TypeError(
                "__init__ takes ParseResults as argument, got " + str(type(xl)))
        self.parse_results = xl
        self.IgnoreIsomerMath = IgnoreIsomerMath
        self.targ = self.setParticleType(xl[0])
        self.proj = self.setParticleType(xl[1])
        self.products = list(map(self.setProduct, xl[2:]))
        self.setResidual()
        self.setProcessType()

    def __str__(self):
        result = str(self.targ) + '(' + str(self.proj) + ','
        result += self.processType + ')'
        if self.residual:
            return result + str(self.residual)
        return result

    def __repr__(self):
        result = repr(self.targ) + '(' + repr(self.proj) + ','
        result += '+'.join(map(repr, self.products)) + ')'
        if self.residual:
            result += repr(self.residual)
        return result.replace("'", "").upper()

    def parse(self, x):
        try:
            return x4process.parseString(x)
        except ParseException as err:
            raise ReactionParsingError(
                'Can not parse process "' +
                x +
                '",\n    got error "' +
                str(err) +
                '"\n   ')

    def setParticleType(self, i):
        """Figures out what a particle i corresponds to, then creates it"""
        if isinstance(i, ParseResults):
            il = i.asList()
        elif isinstance(i, list):
            il = i
        elif isinstance(i, str):
            if i in ['ELEM', 'MASS', 'ELEM/MASS', 'X', 'NPART']:
                return X4VariableParticle(i)
            else:
                return X4Particle(i)
        else:
            raise TypeError
        if len(il) == 3:
            if il[2].isdigit():
                if il[2] == '0':
                    return X4Element(i)
                else:
                    return X4Nucleus(i)
        elif len(il) > 3:
            return X4Isomer(i, self.IgnoreIsomerMath)
        elif len(il) == 2:
            return X4Particle(i)
        else:
            if len(il) == 1 and len(il[0]) > 4:
                return X4ChemicalCompound(i[0])
            else:
                return X4Particle(i)

    def setProduct(self, i):
        """Figures out what the product of a reaction is, whether it is one or more particles or whether it is a catch-all (e.g. Nonelastic)"""
        if i in list(x4ReactionMap.keys()):
            return i
        return self.setParticleType(i)

    def setResidual(self):
        """Figures out if it is possible for this process to uniquely give a residual and if so, what it is"""
        # Make sure don't have natural target
        can_compute_residual = self.targ.getA() != 0
        # If reaction is Elastic, this is easy, but may have to clean up product list
        for channel in ['EL', 'Elastic', 'SCT', 'Scattering',
                        'THS', 'ThermalScattering', 'INL', 'Inelastic']:
            if channel in self.products:
                self.products = [channel]
                self.residual = self.targ
                return
        # Compute total Z & A in projectile and target
        Zin = self.targ.getZ() + self.proj.getZ()
        Ain = self.targ.getA() + self.proj.getA()
        # Compute total Z & A in product list
        Zout = 0
        Aout = 0
        for prod in self.products:
            if (isinstance(prod, X4Nucleus) or isinstance(prod, X4Particle)) and Ain > Zin:
                Zout += prod.getZ() # TODO: Probably a bug 
                Aout += prod.getA()
            else:
                can_compute_residual = False
        # If residual specified Z's and A's will match
        if Zin == Zout and Ain == Aout:
            self.residual = self.products.pop(len(self.products) - 1)
        elif can_compute_residual:
            try:
                self.residual = X4Nucleus(
                    [str(Zin - Zout), endl_ZSymbol(Zin - Zout), str(Ain - Aout)])
            except AttributeError:
                if (Zin - Zout) == -1 and (Ain - Aout) == 0:
                    self.residual = X4Particle('E')
                elif (Zin - Zout) == +1 and (Ain - Aout) == 0:
                    self.residual = X4Particle('B+')
                elif abs(Zin - Zout) > 1000 or abs(Ain - Aout) > 1000:
                    self.residual = None
                else:
                    raise ResidualNucleusError("Cannot compute residual, Delta Z = " + str(
                        Zin - Zout) + ", Delta A = " + str(Ain - Aout) + ", for reaction " + str(self.parse_results))
        else:
            self.residual = None
        # remove residual from product list in case of double entries
        if self.residual in self.products:
            self.products.remove(self.residual)

    def setProcessType(self):
        """Figures out what the process type is from the products list"""
        def swapit(i):
            if i in x4ReactionMap:
                return x4ReactionMap[i]
            return i
        self.processType = '+'.join(map(str, list(map(swapit, self.products))))


class X4Measurement:
    """Parsed Exfor measurement.  This is a dummy class to organize the reaction or reaction combo classes"""

    def __init__(self, pointer, comment):
        pass


class X4Reaction(X4Process, X4Measurement):
    """Parsed Exfor reaction.  This is a process, plus all the modifiers that follow it (e.g. "SIG" or "NU")"""

    def __init__(self, x, IgnoreIsomerMath=False):
        if isinstance(x, str):
            x = self.parse(x)
        X4Process.__init__(self, x[0], IgnoreIsomerMath)
        self.quantity = x[1:]

    def __str__(self):
        return self.getReactionType() + ' for ' + X4Process.__str__(self)

    def __repr__(self):
        return '(' + X4Process.__repr__(self) + ',' + ','.join(self.quantity) + ')'

    def parse(self, x):
        try:
            return x4reaction.parseString(x)
        except ParseException as err:
            if "/" in x or "+" in x or "//" in x:
                raise IsomerMathParsingError(
                    'Reaction ' + x + ' looks like it contains "isomer math"')
            raise ReactionParsingError(
                'Can not parse reaction "' +
                x +
                '",\n    got error "' +
                str(err) +
                '"\n   ')

    def has_quantity(self, i):
        return i in self.quantity

    def getReactionType(self):
        # Try most general quantity
        result = ','.join(self.quantity)
        if result in list(x4QuantityMap.keys()):
            return x4QuantityMap[result][0]
        # Didn't work, try taking list apart
        result = ''
        for i in self.quantity:
            if i in list(x4ModifierMap.keys()):
                result = x4ModifierMap[i][0] + ' '
                break

        def addcomma(x): return ',' + x
        for i in self.quantity + list(map(addcomma, self.quantity)):
            if i in list(x4QuantityMap.keys()):
                result += x4QuantityMap[i][0]
                break
        return result


class X4ReactionCombination(X4Measurement):
    """Parsed Exfore reaction combination.  This is what is measured when """

    def __init__(self, x):
        if isinstance(x, str):
            x = self.parse(x)
        # Extract part of line contained in either a reaction or mathematical expression
        self.data = list(map(self.getStrOrX4Reaction, x))
        self.reaction_list = self.getReactionList()
        self.quantity = "Coupled"
        self.processType = 'Coupled'

    def parse(self, x):
        try:
            return x4compound_expression.parseString(x)
        except ParseException as err:
            raise ReactionParsingError(
                'Can not parse compound reaction expression "' +
                x +
                '",\n    got error "' +
                str(err) +
                '"\n   ')

    def getStrOrX4Reaction(self, i):
        if i in ['(', ')', '+', '-', '*', '/', '=', '//']:
            return i
        else:
            try:
                return X4Reaction(i)
            except (IsomerMathParsingError):
                return X4ReactionIsomerCombination(i)

    def getReactionList(self):
        """assemble a list of all the reactions in self.data"""
        result = []
        for x in self.data:
            if isinstance(x, X4Reaction):
                result.append(x)
            elif isinstance(x, X4ReactionIsomerCombination):
                result += x.getReactionList()
        return result

    def has_quantity(self, i):
        if len(self.reaction_list) < 1:
            raise TypeError("Reaction list too short in X4ReactionCombination")
        for r in self.reaction_list:
            if r.has_quantity(i):
                return True
        return False

    def __str__(self): return self.print_gizmo(str)

    def __repr__(self): return self.print_gizmo(repr)

    def print_gizmo(self, op):
        ans = ''
        if self.data is None:
            return ans
        for j in self.data:
            if str(j) in ['(', ')', '+', '-', '*', '/', '=', '//']:
                ans += j
            else:
                ans += '( ' + op(j) + ' )'
        return ans


class X4ReactionIsomerCombination(X4ReactionCombination):

    def __init__(self, x):
        '''Repack x to unravel the isomer math, then delegate to the X4ReactionCombination constructor'''
        if isinstance(x, str):
            x = self.parse(x)
        x = self.repack(x)
        X4ReactionCombination.__init__(self, x)

    def repack(self, x):
        '''
        Repacks an instance of isomer math as a reaction combination.  It does this by ::

            - disassembling the list of parts of the reaction
            - disassemble the residual coding to pull apart the isomer math from the isomers themselves
            - reassemble the reactions as the list you'd get if this was a reaction combination
        '''
        # disassemble the list of parts of the reaction
        if len(x) == 1:
            x = x[0]
        uglyRxn = x[0]
        # ... non-trivial quants ...
        quant = x[1]
        if ',' not in quant:
            quant = ',' + quant
        # ... possible isomer projectiles ...
        if len(uglyRxn[0]) > 3:
            targ = '-'.join(uglyRxn[0][0:3]) + '-' + ''.join(uglyRxn[0][4:])
        else:
            targ = '-'.join(uglyRxn[0])
        # ... maybe heavy-ion projectiles ...
        if isinstance(uglyRxn[1], str):
            proj = uglyRxn[1]
        else:
            proj = '-'.join(uglyRxn[1])
        # ... lots of products ...
        proc = []
        for protoProc in uglyRxn[2:-1]:
            if isinstance(protoProc, str):
                proc.append(protoProc)
            else:
                proc.append(''.join(protoProc))
        proc = '+'.join(proc)
        # ... and then the isomer math ...
        uglyResid = uglyRxn[-1]

        # disassemble the residual coding
        residPrefix = uglyResid[0:3] + [uglyResid[4]]
        residList = [residPrefix]
        for thing in uglyResid[5:]:
            if thing in ['-', '+', '=', '/', '//']:
                residList.append(thing)
            elif thing in ['0', '1', '2', '3', '4', '5']:
                residList[-1][-1] += thing
            else:
                residList.append(residPrefix[0:-1] + [thing])

        # reassemble the reactions as the list you'd get if this was a reaction
        # combination
        result = []
        for residPart in residList:
            if isinstance(
                    residPart, list):  # we have a new residual, therefore a new reaction
                result.append('(' + targ + '(' + proj + ',' + proc + ')' +
                              '-'.join(residPart) + ',' + quant + ')')
            else:  # the math symbol separating two parts of a string
                result.append(residPart)
        return '(' + ''.join(result) + ')'


# ------------------------------------------------------
# Main
# ------------------------------------------------------
if __name__ == "__main__":
    # ---------------------------------
    print()
    print(10 * '*' + ' parse nuclei ' + 10 * '*')
    for i in ["94-PU-240", "94-Pu-240", "94-PU-240-",
              "94-PU-240-M", "94-Pu-240-M2", "94-Pu-240-G+M"]:
        il = x4nucleus.parseString(i)
        za = X4Nucleus(il)
        print(i.ljust(20), str(il).ljust(40), repr(za).ljust(
            20), za.endlZAStyle().ljust(20), za.exforStyle().ljust(20))
    # ---------------------------------
    print()
    print(10 * '*' + ' process particle ' + 10 * '*')
    for i in ["PI", "N", "A", "HE3"]:
        il = x4particle.parseString(i)
        print(i.ljust(10), str(il).ljust(15), X4Particle(il))
    # ---------------------------------
    print()
    print(10 * '*' + ' parse process ' + 10 * '*')
    for i in ["(N,2n)", "(N,N)94-PU-240", "(N,TOT)", "(N,F)", "(P,2p+4n)", "(94-PU-240,X)",
              '(0,F)', '(P,A+6-C-14+4N)', '(P,A+6-C-14+4N+X)']:  # has trouble with isomer targets
        ii = "94-PU-240" + i
        il = x4process.parseString(ii)
        print(ii.ljust(30), str(il).ljust(70), X4Process(il))
    # ---------------------------------
    print()
    print(10 * '*' + ' parse reactions ' + 10 * '*')
    for i in ["(94-PU-239(N,F),,SIG)", "(92-U-238-M(0,F),TER,AKE,LCP)",
              "(94-PU-239(N,ABS),,SIG,,MXW)", "(94-PU-239(P,A+6-C-14+4N),,SIG)", "(94-PU-240(N,0),,EN)"]:
        res = x4reaction.parseString(i)
        print(i.ljust(35), str(res).ljust(70), X4Reaction(res))
    # ---------------------------------
    print()
    print(10 * '*' + ' parse compound ' + 10 * '*')
    # def test( str ):
    #    global exprStack
    #    exprStack = []
    #    ans = crackX4Compound().parseString(str)
    #    print str
    #    print ans
    #    #print exprStack  #need python2.3 to make this work
    for i in [
            "(((94-PU-239(N,F),,SIG)-(92-U-238-M(0,F),TER,AKE,LCP))/(94-PU-239(N,ABS),,SIG,,MXW))"]:
        #    test(i)
        print(i, '\n', x4compound_expression.parseString(i))
        for j in x4compound_expression.parseString(i):
            print(j)
    # ---------------------------------
    print()
    print(10 * '*' + ' process compound ' + 10 * '*')
    for i in [
            "(((94-PU-239(N,F),,SIG)-(92-U-238-M(0,F),TER,AKE,LCP))/(94-PU-239(N,ABS),,SIG,,MXW))"]:
        #    test(i)
        ans = ''
        for j in x4compound_expression.parseString(i):
            if str(j) in ['(', ')', '+', '-', '*', '/']:
                ans += j
            else:
                ans += '( ' + str(X4Reaction(j)) + ' )'
        print(ans)
    # ---------------------------------
    print()
    print(10 * '*' + ' REAL TEST ' + 10 * '*')
    infile = file('Testing/test_rxn_strings.txt', mode='r')
    lines = infile.readlines()
    infile.close()
    rxnfieldlist = []
    pointers = {}
    lastfield = ''
    for line in lines:
        if line[0:8] == 'REACTION' or line[10] != ' ':
            rxnfieldlist.append(lastfield)
            lastfield = line[11:66].strip()
            if line[10] != ' ':
                pointers[len(rxnfieldlist) - 1] = line[10]
        else:
            lastfield += ' ' + line[11:66].strip()
    rxnfieldlist.append(lastfield)
    rxnfieldlist.pop(0)

    for line in rxnfieldlist:
        iline = rxnfieldlist.index(line)
        print('Reaction field #', iline, ':')
        if iline in list(pointers.keys()):
            print('has pointer ', pointers[iline])
        print(line)
        print(x4reactionfield.parseString(line))
