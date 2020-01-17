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

# module exfor_utils.py
"""
exfor_utils module - Classes, Methods and Utility functions to aid in parsing Exfor formatted data
"""
from .exfor_dicts import X4DictionaryServer
from .exfor_exceptions import BrokenNumberError

# ------------------------------------------------------
# Common data
# ------------------------------------------------------
#DataSectionTags = ( 'DATA', 'COMMON' )
#TagPrefixes     = ( 'NO', 'END' )
#SystemTags      = ( 'TRANS', 'ENTRY', 'SUBENT', 'BIB', 'COMMON', 'DATA', 'REQUEST' )
x4Dictionaries = X4DictionaryServer().getAllDictionaries()
COMMENTSTRING = '#'
VERBOSE = False


# ---------- formatExceptionInfo ----------
def formatExceptionInfo(maxTBlevel=5):
    import traceback, sys
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)


# ---------- timeit ----------
def timeit(method):
    '''
    A timing decorator.  Use it like this:

        >>> @timeit
        >>> def f1():
        >>>    time.sleep(1)
        >>>    print 'f1'

    '''
    import time

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te - ts))
        return result
    return timed


# ---------- comparison functions with abs & rel tolerances ----------
def withinXPercent(a, b, percent=1.0, absTol=1e-14):
    if a + b == 0.0:
        return True
    if abs(a) + abs(b) < absTol:
        return True
    return abs(a - b) * 2.0 / abs(a + b) <= percent / 100.0


def allWithinXPercent(aL, bL, percent=1.0, absTol=1e-14):
    if len(aL) != len(bL):
        return False
    return all([withinXPercent(*x, percent=percent, absTol=absTol) for x in zip(aL, bL)])


# ---------- unique ----------
def unique(l):
    newl = []
    for x in l:
        if not x in newl:
            newl.append(x)
    return newl


# ---------- parseFORTRANNumber ----------
def parseFORTRANNumber(numstring):
    """
    Parses a number string in the 50 or so variations seen in the Exfor data
    @type  numstring: string
    @param numstring: String containing the potential number
    @rtype:      number
    @return:     the hopefully correctly parsed number
    """
    if numstring.strip() == '':
        return None
    try:
        return float(numstring)
    except BaseException:
        # rip out extra space on ends
        tmp = numstring.strip()
        if tmp == "":
            return 0
        # cures the missing E problem
        if tmp.count('E') < 1 and (tmp[-3:].count('+') + tmp[-3:].count('-') >= 1):
            if tmp[-3:].count('-') == 1:
                separator = '-'
            else:
                separator = '+'
            tmp = tmp[:-3] + tmp[-3:].replace(separator, 'E' + separator)
        # cures the missing digits problem
        tmp = tmp.replace(' ', '')
        try:
            return float(tmp)
        except BaseException:
            raise BrokenNumberError(numstring)


# ---------- chunkifyX4Request ----------
def chunkifyX4Request(request):
    """
    Gizmo to break a raw Exfor request (in the form of a list of strings) into a list of Exfor entries (themselves just lists of strings)
    @type  request: list of strings
    @param request: Exfor Request to be chopped into Exfor Entries
    @rtype: list of list of strings
    @return: list of list of strings w/ innermost list of strings assumed to be Exfor Entries
    """
    if not isinstance(request, type([])):
        raise TypeError

    entries = []
    inEntry = False
    entry = []

    for line in request:
        if inEntry:
            entry.append(line)
            if line[0:11].strip() == 'ENDENTRY':
                entries.append(entry)
                inEntry = False
        else:
            if line[0:11].strip() == 'ENTRY':
                inEntry = True
                entry = []
                entry.append(line)
    return entries


def list_of_dicts_to_table(list_of_dicts, cols=None):
    # build up the columns based on the dictionary contents if a list of columns not given
    if cols is None:
        cols = []
        for i in list_of_dicts:
            for k in i:
                if not k in cols:
                    cols.append(k)
    # now fill the table
    table = []
    for i in list_of_dicts:
        table.append([i.get(k, None) for k in cols])
    return cols, table


def latex_format_table(cols, table): pass


def prettyprint_table(colLabels, table, colwidth=20):
    print(' '.join([str(x).ljust(colwidth) for x in colLabels]))
    for row in table:
        print(' '.join([str(x).ljust(colwidth) for x in row]))
