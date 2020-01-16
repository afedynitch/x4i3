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

#!/usr/bin/python
# module exfor_exceptions.py
"""
exfor_exceptions module - Exceptions for Exfor interface
"""

# -------------------------------------------
#
# Various Field Parsing Errors
#
# -------------------------------------------


class ReferenceParsingError(Exception):
    """Base class for all reference parsing exceptions"""

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class AuthorParsingError(Exception):
    """Base class for all author parsing exceptions"""

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InstituteParsingError(Exception):
    """Base class for all author parsing exceptions"""

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ParticleParsingError(Exception):
    """Base class for all particle parsing exceptions"""

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)

# -------------------------------------------
#
# ReactionParsingError(s)
#
# -------------------------------------------


class ReactionParsingError(Exception):
    """Base class for all reaction parsing exceptions"""

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IsomerMathParsingError(Exception):
    """Raise this when someone has math expressions in the isomer spot (e.g. 94-Pu-240-M1+M2)"""

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


# -------------------------------------------
#
# ResidualNucleusError
#
# -------------------------------------------
class ResidualNucleusError(ReactionParsingError):
    """Raise this if you can't figure out the residual nucleus"""

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


# -------------------------------------------
#
# DataSectionParsingError
#
# -------------------------------------------
class DataSectionParsingError(Exception):
    """Base class for all data parsing exceptions"""

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


# -------------------------------------------
#
# BrokenNumberError
#
# -------------------------------------------
class BrokenNumberError(DataSectionParsingError):
    """Raise this when you get a badly formatted number"""

    def __init__(self, value=''):
        self.value = 'Badly formatted number: "' + repr(value) + '"'

# -------------------------------------------
#
# BadUnitsError
#
# -------------------------------------------


class BadUnitsError(DataSectionParsingError):
    """Raise this when you get units no one can use"""

    def __init__(self, value=''):
        self.value = 'Bad units: "' + repr(value) + '"'

# -------------------------------------------
#
# UserInterventionRequired
#
# -------------------------------------------


class UserInterventionRequired(Exception):
    def __init__(self, value=''):
        if len(value) == 8:
            self.value = [value[0:5] + '001', value]
        elif len(value) == 5:
            self.value = value


# -------------------------------------------
#
# NoUncertaintyGivenError
#
# -------------------------------------------
class NoUncertaintyGivenError(DataSectionParsingError):
    def __init__(self, value=''):
        self.value = 'No uncertainty column for ' + repr(value)


# -------------------------------------------
#
# NoHopeForUncertaintyError
#
# -------------------------------------------
class NoHopeForUncertaintyError(DataSectionParsingError):
    def __init__(self, value=''):
        self.value = 'No hope for extracting a uncertainty column in ' + repr(value)


# -------------------------------------------
#
# NoValuesGivenError
#
# -------------------------------------------
class NoValuesGivenError(DataSectionParsingError):
    def __init__(self, value=''):
        self.value = 'No value column for ' + repr(value)
