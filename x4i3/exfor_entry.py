# Modifications to this file have this license
# Copyright (c) 2020, Anatoli Fedynitch <afedynitch@gmail.com>

# This file is part of the fork (x4i3) of the EXFOR Interface (x4i)

# Please read the LICENCE.txt included in this distribution including "Our [LLNL's]
# Notice and the GNU General Public License", which applies also to this fork.

# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License (as published by the
# Free Software Foundation) version 2, dated June 1991.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# terms and conditions of the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

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

# module exfor_entry.py
"""
exfor_entry module 
"""
from x4i3 import exfor_subentry
from x4i3 import exfor_dataset
from x4i3 import exfor_exceptions
import os
from x4i3.exfor_utilities import COMMENTSTRING
from x4i3 import DATAPATH, fullDBPath


def x4EntryFactory(enum, subentsList=None, rawEntry=False, customDBPath=None):
    '''
    This function takes an EXFOR ENTRY number (enum), retrieves the corresponding file 
    from disk, and constructs a valid X4Entry.  The rawEntry=True flag returns optionally 
    just the unparsed list of SUBENTs, each as strings.
    '''
    if len(enum) != 5:
        raise ValueError(
            "A valid EXFOR ENTRY is a string with exactly 5 characters")
    result = []  # the entry, split into subentries

    dbPath = fullDBPath if customDBPath is None else customDBPath
    try:
        with open(os.path.join(dbPath, enum[:3], enum + '.x4'),
            mode='r', newline=None, encoding='latin1') as f:
            entry = f.readlines()
    except TypeError:
        with open(os.path.join(dbPath, enum[:3], enum + '.x4'),
            mode='rU') as f:
            entry = f.readlines()
    subent = ''
    for line in entry:
        if line.startswith('ENTRY') or line.startswith('ENDENTRY') or line.startswith('NOSUBENT'):
            pass
        elif line.startswith('SUBENT'):
            subent = line
        else:
            subent += line
        if line.startswith('ENDSUBENT'):
            if subentsList == None or subent[14:22].strip() in subentsList:
                result.append(subent)
            subent = ''
    if rawEntry:
        return result
    return X4Entry(result)


def x4DictionaryEntryFactory(enum, subentsList=None, rawEntry=False):
    '''
    This function takes an EXFOR ENTRY number (enum), loads the compressed dictionary of
    x4 file contents, and constructs a valid X4Entry.  The rawEntry=True flag returns optionally 
    just the unparsed list of SUBENTs, each as strings. Th
    '''
    # global __database_dict
    from x4i3 import database_dict
    if len(enum) != 5:
        raise ValueError(
            "A valid EXFOR ENTRY is a string with exactly 5 characters: ", enum, len(enum))
    result = []  # the entry, split into subentries

    #entry = open( os.sep.join( [ DATAPATH, 'db', enum[:3], enum + '.x4' ] ), mode = 'rU' ).readlines()
    entry = database_dict[enum[:3] + '/' + enum + '.x4']
    subent = ''
    for line in entry:
        if line.startswith('ENTRY') or line.startswith('ENDENTRY') or line.startswith('NOSUBENT'):
            pass
        elif line.startswith('SUBENT'):
            subent = line
        else:
            subent += line
        if line.startswith('ENDSUBENT'):
            if subentsList == None or subent[14:22].strip() in subentsList:
                result.append(subent)
            subent = ''
    if rawEntry:
        return result
    return X4Entry(result)


def extractX4EntryIndex(entry):
    """
    Grabs the entry number from the "ENTRY" line of an EXFOR entry
    @type  entry: list of strings
    @param entry: list of string containing the Exfor entry
    @rtype: string or None
    @return: the entry index as specified by Exfor
    """
    for line in entry:
        if line.strip() == "":
            continue
        if line.split()[0] == "ENTRY":
            return line[14:22].strip()
        if line.split()[0] == "SUBENT":
            return line[14:22][0:5]  # this'll work too
    return None


class X4Entry(dict):
    """
    An EXFOR Entry is composed of X4SubEntries
    """

    def __init__(self, raw_entry):
        '''Expect raw_entry to be a valid list of strings, with each string being one subentry'''
        self.accnum = extractX4EntryIndex(raw_entry)
        if type(self.accnum) != str or len(self.accnum) != 5:
            raise KeyError(
                'Invalid EXFOR Accnum: should have 5 characters, found ' + str(self.accnum))
        self.errors = {}
        for x in raw_entry:
            try:
                subent = exfor_subentry.X4SubEntry(x)
                self[subent.accnum] = subent
            except IndexError as err:
                raise IndexError(
                    str(err)+' while processing "'+str(x[:22])+'"')

    def __repr__(self):
        '''A string representation that should match what comes from IAEA and should be suitable for parsing with x4i'''
        result = 'ENTRY'.ljust(11) + self.accnum.ljust(11) + '\n'
        for key in self.sortedKeys():
            result += repr(self[key]) + '\n'
        result += 'ENDENTRY'.ljust(11)
        return result

    def __str__(self):
        '''Possibly prettier version of the string representation that should match what comes from IAEA and should be suitable for parsing with x4i'''
        result = 'ENTRY'.ljust(11) + self.accnum.ljust(11) + '\n'
        for key in self.sortedKeys():
            result += str(self[key]) + '\n'
        result += 'ENDENTRY'.ljust(11)
        return result

    def __getitem__(self, i):
        '''Allow getting subentry using a str or int including either the full EXFOR subentry code or just the last 3 digits'''
        if type(i) == int:
            i = str(i)
        if len(i) == 8:
            return dict.__getitem__(self, i)
        elif len(i) <= 3:
            return dict.__getitem__(self, self.accnum + i.zfill(3))
        else:
            raise KeyError('Invalid SubEntry index :' + i)

    def chunkify(self, oldentry):
        """
        Takes a list of strings, assumed to be an Exfor Entry and returns a list of SubEntries
        @type  oldentry: list of strings
        @param oldentry: Exfor Entry to be chopped into SubEntries
        @rtype: list of list of strings
        @return: list of list of strings w/ innermost list of strings assumed to be Exfor SubEntries
        """
        if type(oldentry) != type([]):
            raise TypeError(
                "Sent something other than a list, namely type "+str(type(oldentry)))

        entry = []
        inSubEntry = False
        subentry = []

        for line in oldentry:
            if inSubEntry:
                subentry.append(line)
                if line[0:11].strip() == 'ENDSUBENT':
                    entry.append(subentry)
                    inSubEntry = False
            else:
                if line[0:11].strip() == 'SUBENT':
                    inSubEntry = True
                    subentry = []
                    subentry.append(line)
        return entry

    def getDataSets(self):
        datasets = {}
        if self.deleted():
            return datasets

        # Get the information common to all subentries
        main_meta = None
        main_reactions = {}
        main_monitors = {}
        main_common = None
        if 'BIB' in self[1]:
            main_meta = self[1]['BIB'].meta(subent=self.accnum + '001')
            if 'REACTION' in self[1]['BIB']:
                main_reactions = self[1]['BIB']['REACTION'].reactions
            if 'MONITOR' in self[1]['BIB']:
                main_monitors = self[1]['BIB']['MONITOR'].reactions
        if 'COMMON' in self[1]:
            main_common = self[1]['COMMON']

        # Loop through the subents in self & make (the correct) X4DataSets for each dataset found
        for subent in list(self.values()):

            # Skip processing if there is no data section in subent
            if 'DATA' not in subent:
                continue

            # Get the bibliography & common data for this subentry
            subent_meta = None
            subent_reactions = {}
            subent_monitors = {}
            subent_common = None
            if 'BIB' in subent:
                subent_meta = subent['BIB'].meta(subent=subent.accnum)
                if 'REACTION' in subent['BIB']:
                    subent_reactions = subent['BIB']['REACTION'].reactions
                if 'MONITOR' in subent['BIB']:
                    subent_monitors = subent['BIB']['MONITOR'].reactions
            if 'COMMON' in subent:
                subent_common = subent['COMMON']
            meta_list = [main_meta, subent_meta]
            common_list = [main_common, subent_common]

            # Build the datasets corresponding to the main_reactions reaction list; this handles the case where all the
            # subentries share the same reaction list
            for p in main_reactions:
                k = (self.accnum, subent.accnum, p)
                try:
                    if p in main_monitors:
                        datasets[k] = exfor_dataset.X4DataSetFactory(
                            quant=main_reactions[p][0].quantity, meta=meta_list, common=common_list, reaction=main_reactions[p], monitor=main_monitors[p], data=subent['DATA'], pointer=p)
                    else:
                        datasets[k] = exfor_dataset.X4DataSetFactory(
                            quant=main_reactions[p][0].quantity, meta=meta_list, common=common_list, reaction=main_reactions[p], data=subent['DATA'], pointer=p)
                except NotImplementedError as err:
                    self.errors[k] = 'Encountered NotImplementedError: ' + \
                        str(err)
                except IndexError as err:
                    self.errors[k] = 'Encountered IndexError:' + str(err)

            # Build the datasets corresponding to this subentry's reaction list; this handles the case where all the
            # subentries have their own reaction lists
            for p in subent_reactions:
                k = (self.accnum, subent.accnum, p)
                try:
                    if p in subent_monitors:
                        datasets[k] = exfor_dataset.X4DataSetFactory(
                            quant=subent_reactions[p][0].quantity, meta=meta_list, common=common_list, reaction=subent_reactions[p], monitor=subent_monitors[p], data=subent['DATA'], pointer=p)
                    else:
                        datasets[k] = exfor_dataset.X4DataSetFactory(
                            quant=subent_reactions[p][0].quantity, meta=meta_list, common=common_list, reaction=subent_reactions[p], data=subent['DATA'], pointer=p)
                except NotImplementedError as err:
                    self.errors[k] = 'Encountered NotImplementedError: ' + \
                        str(err)
                except IndexError as err:
                    self.errors[k] = 'Encountered IndexError:' + str(err)
        return datasets

    def getSimplifiedDataSets(self, makeAllColumns=False):
        datasets = self.getDataSets()
        for k in datasets:
            try:
                datasets[k] = datasets[k].getSimplified(
                    makeAllColumns=makeAllColumns)
            except NotImplementedError as err:
                self.errors[k] = 'Encountered NotImplementedError: ' + str(err)
            except exfor_exceptions.NoValuesGivenError as err:
                self.errors[k] = 'Encountered NoValuesGivenError: ' + str(err)
            except exfor_exceptions.NoUncertaintyGivenError as err:
                # typicalNoErrorIndicators = [\
                    # 'no information on uncertainties',\
                    # 'errors are not specified',\
                    # 'no information',\
                    # 'error, when given, is not specified',\
                    # 'not given.',\
                    # 'no information given.',\
                    # 'no further information',\
                    # 'no errors given',\
                    # 'nothing given',\
                    # 'no details given',\
                    # 'errors are not given'\
                # ]
                # def checkForNoErrorInfo( x ):
                    # xlow=' '.join( x ).lower()
                    # for i in typicalNoErrorIndicators:
                        # if i in xlow: return True
                    # return False
                # if  not self.doc_subentry['BIB'].has_key('ERR-ANALYS') and not self.raw_subentry['BIB'].has_key('ERR-ANALYS') and not self.hasCommon(): raise NoHopeFordyInCrossSectionError(self.accnum)
                # elif self.doc_subentry['BIB'].has_key('ERR-ANALYS') and checkForNoErrorInfo(self.doc_subentry['BIB']['ERR-ANALYS'].data): raise NoHopeFordyInCrossSectionError(self.accnum)
                # elif self.raw_subentry.has_key('BIB'):
                    # if self.raw_subentry['BIB'].has_key('ERR-ANALYS') and checkForNoErrorInfo(self.raw_subentry['BIB']['ERR-ANALYS'].data): raise NoHopeFordyInCrossSectionError(self.accnum)
                # else : raise NodyInCrossSectionError(self.accnum)
                self.errors[k] = 'Encountered NoUncertaintyGivenError: ' + \
                    str(err)
            except exfor_exceptions.BrokenNumberError as err:
                self.errors[k] = 'Encountered BrokenNumberError:' + str(err)
            except TypeError as err:
                self.errors[k] = 'Encountered TypeError:' + str(err)
            except IndexError as err:
                self.errors[k] = 'Encountered IndexError:' + str(err)
        return datasets

    def sortedKeys(self):
        k = list(self.keys())
        k.sort()
        return k

    def deleted(self):
        if 'HISTORY' in self[1]['BIB']:
            return 'ENTRY DELETED' in self[1]['BIB']['HISTORY']
        return False

    def meta(self): return X4EntryMetaData(self)


class X4EntryMetaData:

    def __init__(self, entry):
        if not isinstance(entry, X4Entry):
            raise TypeError(
                "X4EntryMetaData.__init__ takes an X4Entry as the argument, got an " + str(type(entry)))
        self.accnum = entry.accnum
        self.deleted = entry.deleted()
        self.subentryaccnums = entry.sortedKeys()
        self.bib_meta = entry[1]['BIB'].meta(subent=self.accnum + '001')

    def xmgraceHeader(self):
        if self.deleted:
            return 'ENTRY ' + str(self.accnum) + ' DELETED'
        retval = '' + COMMENTSTRING + 'Exfor Entry ' + \
            self.accnum + '\n' + self.bib_meta.xmgraceHeader()
        return retval

    def citation(self):
        if self.deleted:
            return 'ENTRY ' + str(self.accnum) + ' DELETED'
        return self.bib_meta.citation().replace('?????.???', self.accnum)

    def legend(self):
        """String suitable for a plot legend"""
        if self.deleted:
            return 'ENTRY ' + str(self.accnum) + ' DELETED'
        return self.bib_meta.legend()
