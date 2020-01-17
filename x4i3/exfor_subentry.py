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

# module exfor_subentry.py
"""
exfor_subentry module -
"""
from . import exfor_section


def extractX4SubEntryIndex(subentry):
    """
    Grabs the subentry number from the "SUBENT" line of an EXFOR subentry
    @type  subentry: list of strings
    @param subentry: list of string containing the Exfor subentry
    @rtype:  string or None
    @return: the subentry index as specified by Exfor
    """
    for line in subentry:
        sline = line.strip().split()
        if sline != [] and sline[0] == "SUBENT":
            return line[14:22]
    return None


def extractX4SectionType(section):
    """
    Extracts the type of Exfor section from the token in cols[0:10] from the first line that has non-white space there
    @type  section: list of strings
    @param section: list of strings to look to find a valid tag
    @rtype: string or None
    @return: string containing the section type.  Is one of 'BIB', 'DATA' or 'COMMON'
    """
    for line in section:
        tag = line[0:10].strip()
        if tag in ('BIB', 'DATA', 'COMMON'):
            return tag
    return None


class X4SubEntry(dict):
    """
    Exfor SubEntry, composed of X4Sections (X4BibSections and X4DataSections)
    """

    def __init__(self, unprocessed_subentry):
        if not isinstance(unprocessed_subentry, list):
            unprocessed_subentry = unprocessed_subentry.split('\n')
        self.accnum = extractX4SubEntryIndex(unprocessed_subentry)
        for section in self.chunkify(unprocessed_subentry):
            tag = extractX4SectionType(section)
            if tag == 'BIB':
                self[tag] = exfor_section.X4BibSection(section)
            elif tag in ('DATA', 'COMMON'):
                self[tag] = exfor_section.X4DataSection(tag, section)
            else:
                raise KeyError(tag + " is not a valid EXFOR Section name")
        self.hascommon = 'COMMON' in self and self['COMMON'] is not None
        self.sorted_keys = list(self.keys())
        self.sorted_keys.sort()

    def __repr__(self):
        '''A string representation that should match what comes from IAEA and should be suitable for parsing with x4i'''
        ans = 'SUBENT'.ljust(11) + self.accnum.ljust(11) + '\n'
        for i in self.sorted_keys:
            ans += repr(self[i]) + '\n'
        ans += 'ENDSUBENT'.ljust(11)
        return ans

    def __str__(self):
        '''Possibly prettier version of the string representation that should match what comes from IAEA and should be suitable for parsing with x4i'''
        ans = 'SUBENT'.ljust(11) + self.accnum.ljust(11) + '\n'
        for i in self.sorted_keys:
            ans += str(self[i]) + '\n'
        ans += 'ENDSUBENT'.ljust(11)
        return ans

    def chunkify(self, oldsubentry):
        """
        Takes a list of strings, assumed to be an Exfor subentry and returns a list of subsections
        @type  oldsubentry: list of strings
        @param oldsubentry: Exfor SubEntry to be chopped into subsections
        @rtype: list of list of strings
        @return: list of list of strings w/ innermost list of strings assumed to be Exfor subsections
        """
        if not isinstance(oldsubentry, list):
            oldsubentry = oldsubentry.split('\n')
        subentry = []
        inSection = False
        section = []
        for line in oldsubentry:
            if inSection:
                section.append(line)
                if line[0:11][0:3] == 'END':
                    subentry.append(section)
                    inSection = False
            else:
                if line[0:11].strip() in ('BIB', 'DATA', 'COMMON'):
                    inSection = True
                    section = []
                    section.append(line)
        return subentry
