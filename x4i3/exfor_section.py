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

# module exfor_sections.py
"""
exfor_sections module -
"""

from . import exfor_utilities
from . import exfor_field
from . import exfor_reactions


class X4Section:
    """
    Base class inserted just to make structure clear.  Stuff in the section remain unparsed.
    """

    def __init__(self, tag='', unprocessed_section=[]):
        self.original = unprocessed_section
        self.tag = tag

    def __str__(self):
        raise NotImplementedError("Implement this in derived class")

    def __repr__(self):
        raise NotImplementedError("Implement this in derived class")


class X4BibSection(X4Section, dict):
    """
    Exfor Bib Section, composed of X4PlainFields
    """

    def __init__(self, unprocessed_section=[]):
        X4Section.__init__(self, 'BIB', unprocessed_section)
        self.sorted_keys = []
        for field in self.chunkify(unprocessed_section):
            ftag = exfor_field.extractX4FieldType(field)
            self.sorted_keys.append(ftag)
            if ftag == 'REACTION':
                self[ftag] = exfor_field.X4ReactionField(field)
            elif ftag == 'MONITOR':
                self[ftag] = exfor_field.X4MonitorField(field)
            elif ftag == 'REFERENCE':
                self[ftag] = exfor_field.X4ReferenceField(field)
            elif ftag == 'AUTHOR':
                self[ftag] = exfor_field.X4AuthorField(field)
            elif ftag == 'TITLE':
                self[ftag] = exfor_field.X4TitleField(field)
            elif ftag == 'INSTITUTE':
                self[ftag] = exfor_field.X4InstituteField(field)
            else:
                self[ftag] = exfor_field.X4PlainField(field)

    def __str__(self):
        ans = self.tag.ljust(11) + str(len(self)).rjust(11) + \
            str(self.totalLen()).rjust(11) + '\n'
        for i in self.sorted_keys:
            ans += str(self[i]) + '\n'
        ans += ('END' + self.tag).ljust(11) + str(self.totalLen()).rjust(11)
        return ans

    def __repr__(self):
        ans = self.tag.ljust(11) + repr(len(self)).rjust(11) + \
            repr(self.totalLen()).rjust(11) + '\n'
        for i in self.sorted_keys:
            ans += repr(self[i]) + '\n'
        ans += ('END' + self.tag).ljust(11) + repr(self.totalLen()).rjust(11)
        return ans

    def chunkify(self, oldsection):
        """
        Takes a list of strings, assumed to be an Exfor 'BIB' section and splits the section into chunks
        @type  oldsection: list of strings
        @param oldsection: Section to be chopped into chunks
        @rtype: list of list of strings
        @return: list of list of strings w/ inner list of strings assumed to be Exfor fields
        """
        if not isinstance(oldsection, list):
            raise TypeError
        section = []
        first = True
        field = []
        for line in oldsection:
            tag = line[0:10].strip()
            if tag not in ('BIB', 'ENDBIB'):
                if first:  # first tag found ...
                    first = False
                elif tag != '':  # found new tag so is new field ...
                    section.append(field)
                    field = []
                field.append(line)
        section.append(field)  # append last field
        return section

    def totalLen(self):
        return sum([self[i].total_len() for i in self])

    def meta(self, subent): return X4BibMetaData(bib=self, subent=subent)


class X4BibMetaData:
    __slots__ = ['year', 'pubType', 'reference', 'institute', 'author', 'title', 'subent']

    def __init__(self, **kw):
        if 'bib' in kw:
            bib = kw['bib']
            if not isinstance(bib, X4BibSection):
                raise TypeError(
                    "X4BibMetaData.__init__ takes an X4BibSection as the argument, got an " + str(type(bib)))
            try:
                self.author = bib['AUTHOR'].authors
            except KeyError:
                self.author = 'None'
            try:
                self.institute = bib['INSTITUTE']
            except KeyError:
                self.institute = 'None'
            self.title = str(bib.setdefault('TITLE'))
            try:
                self.reference = bib['REFERENCE']
                self.pubType = self.reference.pubtype
                self.year = self.reference.pubyear
            except KeyError:
                self.reference = "None"
                self.pubType = "None"
                self.year = "None"
        else:
            self.year = kw.get('year', 'None')
            self.pubType = kw.get('pubType', 'None')
            self.reference = kw.get('reference', 'None')
            self.institute = kw.get('institute', 'None')
            self.author = kw.get('author', 'None')
            self.title = kw.get('title', '')
        self.subent = kw.get('subent', '????????')

    def xmgraceHeader(self):
        retval = '' + exfor_utilities.COMMENTSTRING + '  Authors:   ' + ', '.join(self.author) + \
                 '\n' + exfor_utilities.COMMENTSTRING + '  Title:     ' + self.title + \
                 '\n' + exfor_utilities.COMMENTSTRING + '  Year:      ' + self.year + \
                 '\n' + exfor_utilities.COMMENTSTRING + '  Institute: ' + str(self.institute) + \
                 '\n' + exfor_utilities.COMMENTSTRING + '  Reference: ' + str(self.reference) + \
                 '\n' + exfor_utilities.COMMENTSTRING + '  Subent:    ' + self.subent
        return retval

    def citation(self):
        if len(self.author) > 2:  # too many authors, must use et al.
            author_string = ', '.join(self.author[0:2]) + ', et al.'
        else:
            author_string = ', '.join(self.author)
        return author_string + ", " + str(self.reference) + ";  Data taken from the EXFOR database, file EXFOR " + \
            self.subent + " dated " + \
            str(self.reference.date) + \
            ", retrieved from the IAEA Nuclear Data Services website."

    def legend(self):
        """String suitable for a plot legend"""
        if len(self.author) > 2:  # too many authors, must use et al.
            author_string = ', '.join(self.author[0:2]) + ', et al.'
            return '(' + self.year + ') ' + author_string
        else:
            return '(' + self.year + ') ' + ', '.join(self.author)

    def __repr__(self):
        retval = '' + 'Authors:   ' + ', '.join(self.author) + \
                 '\n' + 'Title:     ' + self.title + \
                 '\n' + 'Year:      ' + self.year + \
                 '\n' + 'Institute: ' + str(self.institute) + \
                 '\n' + 'Reference: ' + str(self.reference) + \
                 '\n' + 'Subent:    ' + self.subent
        return retval


class X4DataSection(X4Section):
    """
    Exfor Data Section
    """

    def __init__(self, tag, unprocessed_section=[]):
        '''

        Data members of this class ::

            - numcols: The number of columns in the data block
            - numrows: The number of logical (or real?) rows in the data block
            - VERBOSELEVEL: Verbosity level flag, probably unused
            - LPR: The number lines in a DATA block per row of real data
            - labels: A Python list of the column labels of the data in each column.
            - units: A Python list of the units of the data in each column.
            - pointers: A Python dict of {pointer:column}
            - raw_data: A Python list of lists containing the data itself as strings
            - data: A Python list of lists containing the data itself, after deFORTRANization
        '''
        X4Section.__init__(self, tag, unprocessed_section)
        # Everything past character 33 is free text and irrelevant
        firstline = unprocessed_section[0][:33].split()
        self.numcols = int(firstline[1])
        self.numrows = int(firstline[2])
        self.VERBOSELEVEL = 0
        # number lines in a DATA block per row of real data!
        self.LPR = (self.numcols - 1) // 6 + 1
        if len(unprocessed_section) != 2 + (self.numrows + 2) * self.LPR:
            if len(unprocessed_section) == 2 + (self.numrows) * self.LPR:
                self.numrows -= 2
                if self.VERBOSELEVEL > 1:
                    print('Column headings were included in datafield size count')
            elif len(unprocessed_section) == 2 + self.numrows:
                self.numrows = self.numrows // self.LPR - 2
                if self.VERBOSELEVEL > 1:
                    print('Datafield size count was set to number of lines in section')
            else:
                print("Additional debugging information:")
                print("   Num. cols.:", self.numcols)
                print("   Num. rows:", self.numrows)
                print("   Lines in each logical row:", self.LPR)
                print("   The unprocess section:\n" + '\n'.join(unprocessed_section))
                raise IndexError('Number of lines in x4DataSection incompatible with information in section tag: ' +
                                 str(len(unprocessed_section)) +
                                 ' vs. ' +
                                 str(2 + (self.numrows + 2) * self.LPR) +
                                 ' or ' +
                                 str(2 + (self.numrows) * self.LPR))
        self.labels = []
        self.units = []
        self.pointers = {}  # map of {pointer:column}
        self.raw_data = []
        self.data = []
        # collapse multi-line rows
        collapsed_section = []
        for i in range(1, len(unprocessed_section) - 1,
                       self.LPR):  # skip begin & end of section tags
            row = ''
            for j in range(self.LPR):
                row += unprocessed_section[i + j][0:67].ljust(66).replace('\n', '')
            collapsed_section.append(row)
        # collect labels, units & pointers
        for j in range(self.numcols):
            self.labels.append(collapsed_section[0][11 * j: 11 * (j + 1)].strip())
            self.units.append(collapsed_section[1][11 * j: 11 * (j + 1)].strip())
            # then it has a pointer because there is something in the 11th column of
            # the field
            if len(self.labels[-1]) == 11:
                p = self.labels[-1][10]
                if not p in self.pointers:
                    self.pointers[p] = []
                self.pointers[p].append(self.labels.index(self.labels[-1]))
        # collect data
        for i in range(self.numrows):
            row = []
            for j in range(self.numcols):
                field = collapsed_section[2 + i][11 * j: 11 * (j + 1)].strip()
                row.append(field)
            self.raw_data.append(row)
            self.data.append(list(map(exfor_utilities.parseFORTRANNumber, row)))

    def __str__(self):
        result = self.tag.ljust(11) + str(self.numcols).rjust(11) + \
            str(self.numrows).rjust(11) + '\n'
        for i in self.labels:
            result += i.ljust(11)
        result += '\n'
        for i in self.units:
            result += i.ljust(11)
        result += '\n'
        for i in self.data:
            for j in i:
                result += str(j).ljust(11)
            result += '\n'
        result += ('END' + self.tag).ljust(11) + str(self.numrows + 2).rjust(11)
        return result

    def __repr__(self):
        '''Should rewrite this so that it breaks at the required line length & wraps correctly'''
        result = self.tag.ljust(11) + str(self.numcols).rjust(11) + \
            str(self.numrows).rjust(11) + '\n'
        for i in self.labels:
            result += i.ljust(11)
        result += '\n'
        for i in self.units:
            result += i.ljust(11)
        result += '\n'
        for i in self.raw_data:
            for j in i:
                result += j.ljust(11)
            result += '\n'
        result += ('END' + self.tag).ljust(11) + str(self.numrows + 2).rjust(11)
        return result

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

    def __len__(self): return self.numrows
