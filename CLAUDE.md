# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

x4i3 is a pure Python interface to the EXFOR (Experimental Nuclear Reaction Data) database maintained by the IAEA. It is a fork of the original x4i (David A. Brown, LLNL), maintained by Anatoli Fedynitch. Licensed GPLv2.

Runtime dependencies: `tqdm`, `requests`. No compiled extensions.

## Build and Test Commands

```bash
# Install in development mode
pip install -e .

# Install with test dependencies
pip install -e ".[tests]"

# Run full test suite (always use --ignore to skip the large data directory)
python -m pytest --pyargs x4i3 --ignore=x4i3/data

# Run a single test file
python -m pytest x4i3/tests/test_exfor_entry.py

# Build source distribution and wheel
pip install build
python -m build
```

## Architecture

The package parses EXFOR-format nuclear data files (a FORTRAN-era structured markup language) and provides programmatic access to the data.

**Database layer:**
- `__init__.py` — Package init, version, database paths, and auto-download logic. On first non-test import, downloads ~600MB database tarball from GitHub releases to `x4i3/data/`. Set `X43I_DATAPATH` env var to override the data directory. Detects `pytest` in `sys.modules` to skip download during testing.
- `exfor_manager.py` — Database manager classes (`X4DBManagerPlainFS` for filesystem access, `X4DBManagerCompressedDictionary` for in-memory cached access). Reads `index.tbl` and pickle caches.

**Parsing layer (EXFOR format → Python objects):**
- `exfor_entry.py` / `exfor_subentry.py` / `exfor_section.py` — Parse EXFOR entries, subentries, and sections
- `exfor_field.py` / `exfor_column_parsing.py` — Field and data column parsing
- `exfor_grammers.py` — pyparsing-based grammar definitions for the EXFOR format
- `exfor_reactions.py` / `exfor_particle.py` — Nuclear reaction and particle definitions
- `exfor_dataset.py` — Dataset extraction from parsed entries

**Support:**
- `exfor_dicts.py` — Dictionary lookups using files in `x4i3/dicts/`
- `pyparsing2.py` / `pyparsing3.py` — Vendored pyparsing modules for compatibility
- `exfor_utilities.py` — Utility functions
- `exfor_exceptions.py` — Custom exception classes

**Tests:**
- `x4i3/tests/` — Test suite with mock EXFOR data in `x4i3/tests/data/` (not the full database)
- Test data files (`12898.x4`, `E0783.x4`) are committed to the repo for unit tests

## Key Conventions

- Always pass `--ignore=x4i3/data` to pytest to avoid scanning the large downloaded database directory.
- The `x4i3/data/` directory is not committed to the repo; it is downloaded at runtime on first import.
- Advanced database management tools live in the separate `x4i3_tools` repository.
