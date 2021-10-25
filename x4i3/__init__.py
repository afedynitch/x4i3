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

# General info
from __future__ import print_function
import os
import sys

MAJOR_VERSION = 1
MINOR_VERSION = 1
PATCH = 0

__package_name__ = "x4i3 -- The Exfor Interface"
__version__ = '.'.join(map(str, [MAJOR_VERSION, MINOR_VERSION, PATCH]))
__author__ = 'David Brown <brown170@llnl.gov>, Anatoli Fedynitch <afedynitch@gmail.com>'
__url__ = 'https://github.com/afedynitch/x4i3'
__license__ = 'GPLv2'
__disclaimer__ = \
    """LLNL Disclaimer:
  This work was prepared as an account of work sponsored by an agency of the
  United States Government. Neither the United States Government nor the
  University of California nor any of their employees, makes any warranty,
  express or implied, or assumes any liability or responsibility for the
  accuracy, completeness, or usefulness of any information, apparatus, product,
  or process disclosed, or represents that its use would not infringe
  privately-owned rights.  Reference herein to any specific commercial products,
  process, or service by trade name, trademark, manufacturer or otherwise does
  not necessarily constitute or imply its endorsement, recommendation, or
  favoring by the United States Government or the University of California. The
  views and opinions of authors expressed herein do not necessarily state or
  reflect those of the United States Government or the University of California,
  and shall not be used for advertising or product endorsement purposes."""

# Common filenames
indexFileName = 'index.tbl'
errorFileName = 'error-entries.pickle'
coupledFileName = 'coupled-entries.pickle'
monitoredFileName = 'monitored-entries.pickle'
reactionCountFileName = 'reaction-count.pickle'
dbPath = 'db'

# URL to the compressed database files on github
url='https://github.com/afedynitch/x4i3/releases/download/last_before_pep8_formatting/x4i3_X4-2021-03-08.tar.gz'
# url='https://github.com/afedynitch/x4i3/releases/download/last_before_pep8_formatting/x4i3_EXFOR-2016-04-01.tar.gz'

# Paths for standard usage
DATAPATH = os.path.abspath(os.path.join(__path__[0], 'data'))
fullIndexFileName = os.path.join(DATAPATH, indexFileName)
fullErrorFileName = os.path.join(DATAPATH, errorFileName)
fullCoupledFileName = os.path.join(DATAPATH, coupledFileName)
fullMonitoredFileName = os.path.join(DATAPATH, monitoredFileName)
fullReactionCountFileName = os.path.join(DATAPATH, reactionCountFileName)
fullDBPath = os.path.join(DATAPATH, dbPath)
dbTagFile = os.path.join(DATAPATH, 
    os.path.splitext(os.path.splitext(os.path.split(url)[1])[0])[0][5:])

# Paths for unit testing only
TESTDATAPATH = os.path.abspath(os.path.join(__path__[0], 'tests', 'data'))  # Mock db for testing
testDBPath = os.path.join(TESTDATAPATH, dbPath)
testIndexFileName = os.path.join(TESTDATAPATH, indexFileName)


def _download_and_unpack_file(url):
    """Downloads the database files created with setup-exfor-db.py as
    a tarball and unpacks them to the correct folder."""

    from tqdm import tqdm
    from glob import glob
    import requests
    import math
    import tarfile
    import tempfile
    import shutil

    # cleanup
    for f in [
        fullIndexFileName, fullErrorFileName,
        fullCoupledFileName, fullMonitoredFileName,
        fullReactionCountFileName, fullDBPath, dbTagFile
    ]:
        try:
            shutil.rmtree(f)
        except NotADirectoryError:
            os.remove(f)
        except FileNotFoundError:
            pass
    # Tag files:
    tag_files = [
        f for tag in ['X4-*', 'EXFOR-*'] for f in glob(os.path.join(DATAPATH, tag))
        ]
    for tagfile in tag_files:
        try:
            os.remove(tagfile)
        except FileNotFoundError:
            pass
        

    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)
    tarname = os.path.basename(url)

    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024 * 1024
    wrote = 0
    tempfile = tempfile.TemporaryFile()
    
    print('Downloading data file', tarname)
    for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size // block_size),
                    unit='MB', unit_scale=True):
        wrote = wrote + len(data)
        tempfile.write(data)
    if total_size != 0 and wrote != total_size:
        raise Exception("ERROR, something went wrong")
    tempfile.flush()
    tempfile.seek(0)
    print('Decompressing archive', tarname)
    wrote = 0
    with tarfile.open(fileobj=tempfile, mode='r') as _tar:
        total = len(_tar.getmembers())
        for member in tqdm(_tar.getmembers(), total=total):
            wrote = wrote + len(data)
            _tar.extract(member, DATAPATH)
    tempfile.close()

    with open(dbTagFile,'wb') as f:
        print('Installed database version', dbTagFile)
        pass

def check_if_exists(path, return_bool=False):
    if return_bool:
        if not os.path.exists(path):
            return False
        else:
            return True    
    if not os.path.exists(path):
        raise IOError('File/Directory', path, 'not found. Check installation.')

# Don't download an unpack the files if the module is just tested
if "pytest" not in sys.modules:
    # Check if all files can be located and redownload the archive
    if not all([check_if_exists(p, return_bool=True) for p in [
        DATAPATH, fullIndexFileName, fullErrorFileName,
        fullCoupledFileName, fullMonitoredFileName,
        fullReactionCountFileName, fullDBPath, dbTagFile]]):
        _download_and_unpack_file(url)

    # Check if all files can be located and raise exception if still not there
    _ = [check_if_exists(p) for p in [
        DATAPATH, fullIndexFileName, fullErrorFileName,
        fullCoupledFileName, fullMonitoredFileName,
        fullReactionCountFileName, fullDBPath, dbTagFile]]

# Applications that query multiple entries subsequently using an in-memory
# dictionary that contains all .x4 files from the db folder can improve performance


class DataBaseCache(dict):
    """Reads all .x4 files from db folder and strres them
    in an in-memory dictionary for faster access"""

    def __init__(self):
        self.__initialized = False

    def __load_cache(self):
        for sd in os.listdir(fullDBPath):
            for x4f in os.listdir(os.path.join(fullDBPath, sd)):
                k = sd + '/' + x4f
                dict.__setitem__(self, k, open(os.path.join(
                    fullDBPath, sd, x4f), 'rb').readlines())
        self.__initialized = True

    def __getitem__(self, key):
        if not self.__initialized:
            self.__load_cache()
        return dict.__getitem__(self, key)


# Does lazy initialization, only loads x4 files into memory on access
database_dict = DataBaseCache()

# The stuff below is not well placed here, bad practice, and will be removed soon.
# from x4i3 import exfor_manager, exfor_entry

# __databaseManager = exfor_manager.X4DBManagerDefault()

# def query(**kw): return __databaseManager.query(**kw)


# def raw_retrieve(**kw): return __databaseManager.retrieve(**kw)


# def retrieve(**kw):
#     rr = {}
#     r = __databaseManager.retrieve(**kw)
#     for k, v in r.items():
#         rr[k] = exfor_entry.X4Entry(v)
#     return rr


__all__ = [
    '__init__', 'exfor_dataset', 'exfor_exceptions', 'exfor_manager', 'exfor_reference',
    'exfor_utilities', 'endl_Z', 'exfor_dicts', 'exfor_field', 'exfor_particle', 'exfor_section',
    'exfor_column_parsing', 'exfor_entry', 'exfor_grammers', 'exfor_reactions', 'exfor_subentry'
]
