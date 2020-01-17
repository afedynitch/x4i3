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

# module exfor_dicts.py
"""
exfor_dicts module - Class and Methods for Server that gives look-up tables for abbreviations in EXFOR files
"""

import os
from . import __path__

# ---------- getDictionary ----------


def getDictionary(filename, VERBOSELEVEL=0):
    if not isinstance(filename, str):
        raise TypeError(
            'Variable filename is supposed to be a string, got a ' + str(type(filename)))
    try:
        f = open(filename)
    except IOError:
        if VERBOSELEVEL > 0:
            print("Dictionary file " + filename + " not found")
        return None

    # Initialize variables (they should get overwritten in the exec()
    # calls below)
    Title = ''
    FieldBreaks = []
    NumFields = 0

    # Replace the exec statements from x4i with string ops
    # since exec behavior is inconsistent between Python 2 and 3
    Title = f.readline().split('=')[-1].strip()
    NumFields = int(f.readline().split('=')[-1].strip())
    s = f.readline().split('=')[-1].strip().replace('[','').replace(']','').split(',')
    FieldBreaks = [int(c) for c in s]
    
    if VERBOSELEVEL > 1:
        print("*** " + Title + " ***")
    FieldBreaks.insert(0, 0)

    # rest of file is dictionary
    d = {}
    for line in f:
        line = line.strip()
        FieldBreaks.append(len(line))
        if line != "":
            fieldlist = []
            for i in range(NumFields):
                fieldlist.append(
                    line[FieldBreaks[i]:FieldBreaks[i + 1]].strip())
            item = []
            for i in range(1, NumFields):
                item.append(fieldlist[i])
            d[fieldlist[0]] = item
        FieldBreaks.pop()
    f.close()
    return d

# -------------------------------------------
#
# X4DictionaryServer
#
# -------------------------------------------


class X4DictionaryServer:

    # ---------- __init__ ----------
    def __init__(self, pathToDictionaryFiles=__path__[
                 0] + os.sep + "dicts" + os.sep):
        self.pathToDictionaryFiles = pathToDictionaryFiles
        self.DictionaryNames = (
            (3, "Institutes"),
            (4, "ReferenceTypes"),
            (5, "Journals"),
            (7, "ConferencesAndBooks"),
            (9, "Compounds"),
            (15, "History"),
            (16, "Status"),
            (17, "Rel_Ref"),
            (18, "Facility"),
            (19, "IncidentSource"),
            (20, "AdditionalResults"),
            (21, "Method"),
            (22, "Detectors"),
            (23, "Analysis"),
            (24, "DataHeadings"),
            (30, "Process"),
            (33, "Particles"),
            (34, "Modifiers"),
            (35, "DataType"),
            (36, "Quantities"),
            (37, "Result"))

    # ---------- __getitem__ ----------

    def __getitem__(self, i):
        """
        Shortcut for getDictionary method
        """
        return self.getDictionary(i)

    # ---------- getDictionaryName ----------
    def getDictionaryName(self, x):
        """
        Look up dictionary name
        @type x: int
        @param x: index of the dictionary
        @rtype: string or None
        @return: name of the dictionary
        """
        if isinstance(x, int):
            for i in self.DictionaryNames:
                if (i[0] == x):
                    return i[1]
        return None

    # ---------- getDictionaryIndex ----------
    def getDictionaryIndex(self, x):
        """
        Look up index for dictionary named "x"
        @type x: string
        @param x: name of the dictionary
        @rtype: int or None
        @return: index of the dictionary
        """
        if isinstance(x, str):
            for i in self.DictionaryNames:
                if (i[1] == x):
                    return i[0]
        return None

    # ---------- getDictionaryFilename ----------
    def getDictionaryFilename(self, x):
        """
        Figure out file name of requested dictionary
        @type x: string or int
        @param x: name or index of the dictionary
        @rtype: string or None
        @return: filename for the dictionary
        """
        if isinstance(x, int):
            for i in self.DictionaryNames:
                if (i[0] == x):
                    return "dict" + repr(i[0]).zfill(2) + ".txt"
        elif isinstance(x, str):
            for i in self.DictionaryNames:
                if (i[1] == x):
                    return "dict" + repr(i[0]).zfill(2) + ".txt"
        return None

    # ---------- getDictionary ----------
    def getDictionary(self, x, VERBOSELEVEL=0):
        """
        Retrieve requested dictionary
        @type x: string or int
        @param x: name or index of the dictionary
        @rtype: matrix
        @return: the dictionary
        """
        filename = self.getDictionaryFilename(x)
        return getDictionary(
            self.pathToDictionaryFiles + filename, VERBOSELEVEL=0)

    # ---------- getAllDictionaries ----------
    def getAllDictionaries(self, VERBOSELEVEL=0):
        """
        Retrieve requested dictionary
        @rtype: map or matrices
        @return: map of dictionaries, key is dictionary name
        """
        if VERBOSELEVEL > 1:
            print('Loading EXFOR Dictionaries:')
        dictmap = {}
        for i in self.DictionaryNames:
            tmp = self.getDictionary(i[0], VERBOSELEVEL=VERBOSELEVEL)
            if tmp is not None:
                dictmap[i[1]] = tmp
        return dictmap
