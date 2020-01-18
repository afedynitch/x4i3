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

from .exfor_utilities import unique, COMMENTSTRING
from .exfor_exceptions import NoValuesGivenError, NoUncertaintyGivenError
from .exfor_section import X4BibMetaData
from .exfor_column_parsing import (condenseColumn,
    incidentEnergyParserList, csDataParserList,
    nubarParserList, spectrumArgumentParserList,
    angleParserList, angDistParserList, outgoingEnergyParserList,
    energyDistParserList)
from .exfor_reactions import X4ReactionCombination
import copy
from functools import reduce
import sys

if sys.version_info < (3, 0, 0):
    pyver = 2
else:
    pyver = 3


class X4DataSet(X4BibMetaData):

    def __init__(self, meta=[None, None], common=[
                 None, None], reaction=None, monitor=None, data=None, pointer=None):
        # Initialize merged meta data, a needlessly complicated
        # process
        X4BibMetaData.__init__(
            self, author="None", institute="None", title="None", pubType="None", year="None")
        for m in meta:
            if m is None:
                continue
            for k in m.__slots__:
                if not getattr(m, k) in [None, "None"]:
                    setattr(self, k, getattr(m, k))
        # Initializing the reaction is easy!
        self.reaction = reaction
        self.monitor = monitor
        # Initializing the data is less so...
        self.labels = []
        self.units = []
        self.data = []
        self.simplified = False
        if reaction is None:
            self.coupled = False
        else:
            self.coupled = isinstance(
                reaction[0], X4ReactionCombination)
        if data is not None:
            self.setData(data, common, pointer)

    def setData(self, data, common=[], pointer=None):
        '''This should set up the data, labels and units such that all columns in all COMMON sections are in self
        and such that all columns in DATA which either have no pointer or matching pointer are in self'''
        # Set up the column labels & units (filter on pointers
        # here...)
        column_offsets = []  # where current dataset's columns begin
        column_filter = []
        for d in common + [data]:
            column_offsets.append(len(self.labels))
            if d is None:
                continue
            other_pointers_columns = []
            for p in [x for x in list(d.pointers.keys()) if x != pointer]: other_pointers_columns += d.pointers[p]
            for icol in range(d.numcols):
                if d.pointers == {} or not icol in other_pointers_columns:
                    column_filter.append(True)
                    self.labels.append(d.labels[icol][0:10].strip())
                    self.units.append(d.units[icol][0:10].strip())
                else:
                    column_filter.append(False)
        # add the data itself
        for irow in range(data.numrows):
            row = column_offsets[2] * [0]
            icol = len(row)
            for x in data.data[irow]:
                if column_filter[icol]:
                    row.append(x)
                icol += 1
            self.data.append(row)
        # now add the common data, there'd better not be pointers
        # here!
        for c in common:
            if c is None:
                continue
            if c.numrows == 1:  # copy the rows to all rows in data
                for irow in range(data.numrows):
                    for icol in range(c.numcols):
                        self.data[irow][column_offsets[common.index(
                            c)] + icol] = c[0, icol]
            else:  # copy to the first numrows
                for irow in range(min(c.numrows, data.numrows)):
                    for icol in range(c.numcols):
                        self.data[irow][column_offsets[common.index(
                            c)] + icol] = c[irow, icol]

    def strHeader(self):
        out = self.xmgraceHeader()
        try:
            out += '\n' + COMMENTSTRING + '  Reaction:  ' + \
                ' '.join(map(str, self.reaction))
        except TypeError as e:
            raise TypeError(str(e) + ', got ' + str(type(self.reaction)
                                                    ) + " with value " + str(self.reaction))
        try:
            if self.monitor is not None:
                out += '\n' + COMMENTSTRING + \
                    '  Monitor(s): ' + \
                    ' '.join(map(str, self.monitor))
        except TypeError as e:
            raise TypeError(str(e) + ', got ' + str(type(self.monitor)
                                                    ) + " with value " + str(self.monitor))
        return out

    def reprHeader(self):
        result = X4BibMetaData.__repr__(
            self) + ' \nReaction:  ' + repr(self.reaction[0])
        if self.monitor is not None and len(self.monitor) > 0:
            result += ' \nMonitor(s):' + \
                repr([x[0] for x in self.monitor])
        result += "\n"
        return result

    def __str__(self):
        def unify_py2py3_str(s):
            if pyver == 2:
                return str(s)
            try:
                return str(float(format(j, '.12g')))
            except:
                return str(s)

        out = self.strHeader()
        out += '\n' + COMMENTSTRING + '        '
        for i in self.labels:
            out += str(i).ljust(14)
        out += '\n' + COMMENTSTRING + '        '
        for i in self.units:
            out += str(i).ljust(14)
        out += '\n        '
        for i in self.data:
            for j in i:
                out += unify_py2py3_str(j).ljust(14)
            out += '\n        '
        return out

    def __repr__(self):
        ans = self.reprHeader() + "["
        ans += "['" + "','".join(self.labels) + "']" + ",\n"
        ans += "['" + "','".join(self.units) + "']"
        for row in self.data:
            ans += ",\n" + "[" + ",".join(map(str, row)) + "]"
        ans += "]"
        return ans

    def sort(self, **kw):
        '''In place sort, see Python documentation for list().sort()'''
        self.data.sort(**kw)

    def getSimplified(self, parserMap=None, columnNames=[
    ], makeAllColumns=False, failIfMissingErrors=False):
        '''Returns a simplified version of self.
        inputs:
            parserMap            = { 'column name 1':parserList1, 'column name 2':parserList2, ... }
            columnNames          = [ 'column name 1', 'column name 2', ... ] #put them in the order *you* want
            makeAllColumns       will make uncertainty columns even if no uncertainties are given on a particular column
            failIfMissingErrors  fail (raising exception) if missing an error column
        '''
        result = copy.copy(self)
        if self.simplified:
            return result
        numrows = result.numrows()
        if parserMap is None:
            return result
        # Check that columnNames in sync with parserMap
        for p in parserMap:
            if not p in columnNames:
                raise KeyError(p + ' not in columnNames')
        # Initialize things
        vals = {}
        errs = {}
        no_errs = {}
        result.data = []
        result.labels = []
        result.units = []
        # initialize val, err values
        for parser in parserMap:
            vals[parser] = reduce(condenseColumn, [i.getValue(self)
                                                   for i in parserMap[parser]])
            errs[parser] = reduce(condenseColumn, [i.getError(self)
                                                   for i in parserMap[parser]])
            no_errs[parser] = errs[parser][2:] == [
                None for i in errs[parser][2:]]
            if vals[parser][2:] == [None for i in vals[parser][2:]]:
                raise NoValuesGivenError(parser)
        # Put the data into the result
        # Make the column headings & units, first
        for column in columnNames:
            result.labels.append(column)
            result.units.append(vals[column][1])
        # Now the column labels & units for the uncertainties
        for column in columnNames:
            if not no_errs[column] or makeAllColumns:
                result.labels.append('d(' + column + ')')
                if no_errs[column]:
                    result.units.append(vals[column][1])
                else:
                    result.units.append(errs[column][1])
        # Now assemble the rows & add them to result.data
        for i in range(2, numrows + 2):
            row = []
            for col in columnNames:
                row.append(vals[col][i])
            for col in columnNames:
                if no_errs[col]:
                    if makeAllColumns:
                        row.append(0.0)
                    elif failIfMissingErrors:
                        raise NoUncertaintyGivenError(col)
                else:
                    row.append(errs[col][i])
            result.data.append(row)
        result.simplified = True
        return result

    def append(self, other):
        if self.labels == [] and self.units == [] and self.data == []:
            self.reaction = copy.copy(other.reaction)
            self.monitor = copy.copy(other.monitor)
            self.labels = copy.copy(other.labels)
            self.units = copy.copy(other.units)
            self.data = copy.copy(other.data)
            self.simplified = copy.copy(other.simplified)
            return
        if self.labels == other.labels and self.units == other.units and str(
                self.reaction[0]) == str(other.reaction[0]):
            for row in other.data:
                self.data.append(copy.copy(row))
        else:
            why = ''
            if self.labels != other.labels:
                why += "Labels don't match: " + \
                    str(self.labels) + ', ' + str(other.labels)
            if self.units != other.units:
                why += "Units don't match: " + \
                    str(self.units) + ', ' + str(other.units)
            if self.reaction != other.reaction:
                why += "Reactions don't match: " + \
                    str(self.reaction[0]) + ", " + \
                    str(other.reaction[0])
            if self.monitor != other.monitor:
                why += "Monitors don't match: " + \
                    str(self.monitor) + ", " + str(other.monitor)
            print("Can't add datasets because " + why)
        return

    def csv(self, f):
        import csv
        try:
            with open(f, 'w', encoding="utf-8") as csvf:
                writer = csv.writer(csvf, lineterminator='\n')
                writer.writerows([self.labels, self.units] + self.data)
        except TypeError:
            with open(f, 'w') as csvf:
                writer = csv.writer(csvf, lineterminator='\n')
                writer.writerows([self.labels, self.units] + self.data)

    def numcols(self): return len(self.labels)

    def numrows(self): return len(self.data)

    def __getitem__(self, xxx_todo_changeme):
        (i, j) = xxx_todo_changeme
        if isinstance(i, str):
            if i == 'LABELS':
                return self.labels[j]
            elif i == 'UNITS':
                return self.units[j]
            else:
                raise KeyError('Invalid index: ' + i)
        else:
            return self.data[i][j]


class X4CrossSectionDataSet(X4DataSet):
    def __init__(self, meta=[None, None], common=[
                 None, None], reaction=None, monitor=None, data=None, pointer=None):
        X4DataSet.__init__(self, meta, common, reaction,
                           monitor, data, pointer)

    def getSimplified(self, makeAllColumns=False,
                      failIfMissingErrors=False):
        return X4DataSet.getSimplified(self,
                                       parserMap={
                                           'Energy': incidentEnergyParserList,
                                           'Data': csDataParserList},
                                       columnNames=['Energy', 'Data'],
                                       makeAllColumns=makeAllColumns,
                                       failIfMissingErrors=failIfMissingErrors)


class X4NubarDataSet(X4DataSet):
    def __init__(self, meta=[None, None], common=[
                 None, None], reaction=None, monitor=None, data=None, pointer=None):
        X4DataSet.__init__(self, meta, common, reaction,
                           monitor, data, pointer)

    def getSimplified(self, makeAllColumns=False,
                      failIfMissingErrors=False):
        return X4DataSet.getSimplified(self, parserMap={'Energy': incidentEnergyParserList, 'Data': nubarParserList}, columnNames=[
                                       'Energy', 'Data'], makeAllColumns=makeAllColumns, failIfMissingErrors=failIfMissingErrors)


class X4SpectrumAveCrossSectionDataSet(X4DataSet):
    def __init__(self, meta=[None, None], common=[
                 None, None], reaction=None, monitor=None, data=None, pointer=None):
        X4DataSet.__init__(self, meta, common, reaction,
                           monitor, data, pointer)
        self.spectrum = None

    def getSimplified(self, makeAllColumns=False,
                      failIfMissingErrors=False):
        return X4DataSet.getSimplified(self,
                                       parserMap={
                                           'Energy': spectrumArgumentParserList, 'Data': csDataParserList},
                                       columnNames=['Energy', 'Data'],
                                       makeAllColumns=makeAllColumns,
                                       failIfMissingErrors=failIfMissingErrors)


class X4ResonanceIntCrossSectionDataSet(X4DataSet):
    def __init__(self, meta=[None, None], common=[
                 None, None], reaction=None, monitor=None, data=None, pointer=None):
        X4DataSet.__init__(self, meta, common, reaction,
                           monitor, data, pointer)

    def getSimplified(self, makeAllColumns=False,
                      failIfMissingErrors=False): raise NotImplementedError()


class X4AnalyzingPowerDataSet(X4DataSet):
    def __init__(self, meta=[None, None], common=[
                 None, None], reaction=None, monitor=None, data=None, pointer=None):
        X4DataSet.__init__(self, meta, common, reaction,
                           monitor, data, pointer)

    def getSimplified(self, makeAllColumns=False,
                      failIfMissingErrors=False): return copy.copy(self)


class X4AngularDistributionDataSet(X4DataSet):
    def __init__(self, meta=[None, None], common=[
                 None, None], reaction=None, monitor=None, data=None, pointer=None):
        X4DataSet.__init__(self, meta, common, reaction,
                           monitor, data, pointer)
        self.referenceFrame = 'Lab'
        for col in self.labels:
            if '-CM' in col:
                self.referenceFrame = "Center of mass"
                break

    def strHeader(self):
        out = X4DataSet.strHeader(self)
        out += '\n' + COMMENTSTRING + '  Frame:     ' + self.referenceFrame
        return out

    def getSimplified(self, makeAllColumns=False,
                      failIfMissingErrors=False):
        return X4DataSet.getSimplified(self,
                                       parserMap={'Energy': incidentEnergyParserList,
                                                  'Angle': angleParserList,
                                                  'Data': angDistParserList},
                                       columnNames=['Energy', 'Angle', 'Data'],
                                       makeAllColumns=makeAllColumns, failIfMissingErrors=failIfMissingErrors)


class X4EnergyDistributionDataSet(X4DataSet):
    def __init__(self, meta=[None, None], common=[
                 None, None], reaction=None, monitor=None, data=None, pointer=None):
        X4DataSet.__init__(self, meta, common, reaction,
                           monitor, data, pointer)
        self.referenceFrame = 'Lab'
        for col in self.labels:
            if '-CM' in col:
                self.referenceFrame = "Center of mass"
                break

    def strHeader(self):
        out = X4DataSet.strHeader(self)
        out += '\n' + COMMENTSTRING + '  Frame:     ' + self.referenceFrame
        return out

    def getSimplified(self, makeAllColumns=False,
                      failIfMissingErrors=False):
        return X4DataSet.getSimplified(self,
                                       parserMap={'Energy': incidentEnergyParserList,
                                                  "E'": outgoingEnergyParserList,
                                                  'Data': energyDistParserList},
                                       columnNames=['Energy', "E'", 'Data'],
                                       makeAllColumns=makeAllColumns, failIfMissingErrors=failIfMissingErrors)


class X4EnergyAngleDistDataSet(X4DataSet):
    def __init__(self, meta=[None, None], common=[
                 None, None], reaction=None, monitor=None, data=None, pointer=None):
        X4DataSet.__init__(self, meta, common, reaction,
                           monitor, data, pointer)

    def getSimplified(self, makeAllColumns=False,
                      failIfMissingErrors=False): raise NotImplementedError()


def X4DataSetFactory(quant, meta=[None, None], common=[
                     None, None], reaction=None, monitor=None, data=None, pointer=None):
    if quant == 'Coupled':
        quant_list = unique(
            [i.quantity for i in reaction[0].reaction_list])
        if len(quant_list) == 1:
            quant = quant_list[0]
        else:
            raise NotImplementedError(
                "Coupled data with different quantities in expression:" + str(reaction[0]))
    if quant == ['SIG']:
        return X4CrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['CN', 'SIG']:
        return X4CrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'DERIV']:
        return X4CrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'FCT']:
        return X4CrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['DI', 'SIG']:
        return X4CrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'EVAL']:
        return X4CrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'EXP']:
        return X4CrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'MXW']:
        return X4SpectrumAveCrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'SPA']:
        return X4SpectrumAveCrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'SFC', 'EVAL']:
        return X4SpectrumAveCrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'SFC', 'EXP']:
        return X4SpectrumAveCrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'SFC']:
        return X4SpectrumAveCrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'FST']:
        return X4SpectrumAveCrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'RTE']:
        return X4SpectrumAveCrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'FIS']:
        return X4SpectrumAveCrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'FIS', 'EVAL']:
        return X4SpectrumAveCrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif quant == ['SIG', 'AV']:
        return X4CrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif 'RI' in quant:
        return X4ResonanceIntCrossSectionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif 'POL/DA' in quant:
        return X4AnalyzingPowerDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif 'DA' in quant:
        return X4AngularDistributionDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif 'NU' in quant:
        return X4NubarDataSet(
            meta, common, reaction, monitor, data, pointer)
    elif 'DE' in quant:
        return X4EnergyDistributionDataSet(
            meta, common, reaction, monitor, data, pointer)
    else:
        #raise NotImplementedError( "Unknown observable quantity: " + ','.join( quant ) )
        return X4DataSet(meta, common, reaction,
                         monitor, data, pointer)
