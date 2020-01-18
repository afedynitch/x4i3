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

# module exfor_grammers.py
"""
exfor_grammers module - Collection of pyparsing grammers for parsing Exfor objects
"""
__version__ = "0.0.1"
__author__ = "David Brown <brown170@llnl.gov>"

import sys

if sys.version_info < (3, 0, 0):
    from .pyparsing2 import (Literal, Optional, Word, Combine, Group,
        delimitedList, alphanums, ZeroOrMore, Forward, restOfLine,
        OneOrMore, nestedExpr, alphas, commaSeparatedList)
else:
    from .pyparsing3 import (Literal, Optional, Word, Combine, Group,
        delimitedList, alphanums, ZeroOrMore, Forward, restOfLine,
        OneOrMore, nestedExpr, alphas, commaSeparatedList)

from .exfor_dicts import X4DictionaryServer

# ------------------------------------------------------
# Generic grammer elements
# ------------------------------------------------------
caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
capsStar = "ABCDEFGHIJKLMNOPQRSTUVWXYZ*"
lowers = caps.lower()
nums = "0123456789"
lpar = Literal("(").suppress()
rpar = Literal(")").suppress()
comma = Literal(",").suppress()
plus = Literal("+")
minus = Literal("-")
mult = Literal("*")
doubleslash = Literal("//")
div = Literal("/")
equals = Literal("=")
dash = Literal("-").suppress()

addop = plus | minus
multop = mult | div
mathop = addop | multop

dashorplus = Literal("+").suppress() ^ Literal('-').suppress()
mathop_noshow = dashorplus ^ Literal(
    '//').suppress() ^ Literal('*').suppress() ^ Literal('/').suppress()

altmultop = mult | doubleslash | div | equals
altaddop = plus | minus

# ------------------------------------------------------
# Define the grammer of an Exfor Reaction Field ...
# ------------------------------------------------------
x4isomer_modifier = Word('mMgGTL', max=1) + Optional(Word(nums))

x4basicparticle = Optional(Literal(
    'X')) + eval('^'.join(['Literal( \"' + x + '\" )' for x in list(X4DictionaryServer()["Particles"].keys())]))
x4particle = Combine(Word(alphas) + Optional(Word(nums)))
x4element = Word(capsStar, alphas, min=1, max=2) ^ Literal(
    "PI") ^ Literal("K0") ^ Literal("PIM") ^ Literal("PIP") ^ Literal("P0")
x4nucleus = Word(nums) + dash + x4element + dash + Word(nums) + \
    ZeroOrMore(mathop + x4isomer_modifier)
x4chemical_compound = eval(
    '^'.join(['Literal( \"' + x + '\" )' for x in list(X4DictionaryServer()["Compounds"].keys())]))

x4projectile = Group(x4nucleus) ^ x4particle ^ Literal('0')
x4target = Group(x4chemical_compound | x4nucleus) ^ Literal(
    "ELEM/MASS") ^ Literal("MASS") ^ Literal("ELEM")
x4residual = Group(x4chemical_compound | x4nucleus) ^ Literal(
    "ELEM/MASS") ^ Literal("MASS") ^ Literal("ELEM") ^ Literal("NPART")
x4product = Group(x4nucleus) ^ x4basicparticle ^ x4particle ^ Group(
    Optional(Word(nums)) + x4particle) ^ Literal('0')

x4products = delimitedList(x4product, "+")

x4process = x4target + lpar + x4projectile + \
    comma + x4products + rpar + Optional(x4residual)
x4reaction_descriptor = Word(alphanums + '/*+-') ^ (lpar +
                                                    Word(alphanums + '/*+-') + rpar)
x4reaction = lpar + delimitedList(Group(x4process) ^
                                  ZeroOrMore(x4reaction_descriptor)) + rpar

x4compound_expression = Forward()
x4compound_factor = (Group(x4reaction)) | ("(" + x4compound_expression + ")")
x4compound_term = x4compound_factor + ZeroOrMore((altmultop + x4compound_factor))
x4compound_expression << x4compound_term + ZeroOrMore((addop + x4compound_term))

x4reactionfield = x4compound_expression + restOfLine
# x4reactionfield = OneOrMore(x4compound_expression)+restOfLine #should
# only be one reaction in a field


x4isomermath = Word(nums) + dash + x4element + dash + Word(nums) + \
    ZeroOrMore(mathop + x4isomer_modifier)
x4isomerresidual = Group(x4isomermath)
x4isomerproduct = Group(x4isomermath) ^ x4basicparticle ^ x4particle ^ Group(
    Optional(Word(nums)) + x4particle) ^ Literal('0')
x4isomerproducts = delimitedList(x4isomerproduct, "+")
x4isomerprocess = x4target + lpar + x4projectile + comma + \
    x4isomerproducts + rpar + Optional(x4isomerresidual)
x4isomerreaction = lpar + \
    delimitedList(Group(x4isomerprocess) ^ ZeroOrMore(x4reaction_descriptor)) + rpar
x4isomermathreactionfield = x4isomerreaction + restOfLine

# ------------------------------------------------------
# Define the grammer of an Exfor Text Field
# ------------------------------------------------------
x4word = Word(alphanums + ",.;+-*/'")
x4minicode = lpar + Word(alphanums + "-/") + rpar
x4phrase = OneOrMore(x4word | x4minicode)
x4code = (
    lpar +
    x4phrase +
    rpar) ^ (
        lpar +
        lpar +
        x4phrase +
        rpar +
        equals +
        lpar +
        x4phrase +
        rpar +
    rpar)
x4codefield = Group(x4code) + ZeroOrMore(x4word)
x4textfield = OneOrMore(Group(x4codefield))

x4authorfield = nestedExpr() + restOfLine
x4authorlist = commaSeparatedList

x4refcode = nestedExpr() + restOfLine
x4refcodetautology = (lpar + nestedExpr() + OneOrMore(equals +
                                                      nestedExpr()) + rpar) + restOfLine
