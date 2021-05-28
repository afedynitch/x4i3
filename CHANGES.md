# Changelog


## x4i3 - 1.2.1 28/05/2021

- Added Python 3.9 to CI
- Test data added to source wheel

## x4i3 - 1.2.0 28/05/2021

- Update to a more recent EXFOR database dated 2021/03/08
- main updates happened under the hood for the x4i3_tools support project
- fixed bug in testing where entries were accidentally pulled from the real DB instead of the test DB

### x4i3 - 1.1.0 19/01/2020

- initial release of the fork x4i3
- compatibility with Python 2 and 3
- DataBaseCache that reads all .x4 files in the db directory into memory. Takes time on first startup (until FS cache kicks in) and requires more RAM (+1.5 GB) but accelerates repeated queries. To use this feature use X4DBManagerCompressedDictionary instead of X4DBManagerPlainFS
- function x4DictionaryEntryFactory that uses this dictionary instead of plain file system
- default database manager continues to use the non-cached version X4DBManagerPlainFS
- get-entry.py flag -c (cached) for using the cached access
- removal of the 2012 copy of pyparsing.py adding the pip package pyparsing to the requirements
- Removal of database maintenance tools and separate distributions as [x4i3_tools](https://github.com/afedynitch/x4i3_tools)  
- mock database in x4i3/tests compressed as tar.gz to reduce the size and number of files
- automatic API documentation api-doc tar.gzipped, since users typically read source code these days
- moved test directory to project root
- removed graph tools from distribution and moved into [x4i3_tools](https://github.com/afedynitch/x4i3_tools) (because I don't yet understand what they do)
- check if all data files are available
- removed "quick access" functions from __init__.py of x4i3 since this is bad practice and can result in circular dependencies
- added get-entry.py to examples but not debugged
- Tests successful using Python 2.7.17 and 3.7.5 on Windows and Linux
- Pyparsing2 and Pyparsing3 modules added since tests with new Pyparsing under Python 2.7
- automatic download and decompression of the data directory

### x4i - 1.0.3, 15/02/2011

- Original release of x4i by David A. Brown (LLNL)
