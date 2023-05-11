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

from x4i3 import exfor_entry, exfor_manager
import argparse


def process_args():
    parser = argparse.ArgumentParser(description="Get an EXFOR entry")
    parser.set_defaults(verbose=True)
    parser.add_argument(
        "-v", action="store_true", dest="verbose", help="enable verbose output"
    )
    parser.add_argument(
        "-q", action="store_false", dest="verbose", help="disable verbose output"
    )
    parser.add_argument(
        "-s", dest="subent", default=None, type=str, help="Subentry to retrieve"
    )
    parser.add_argument(
        "-e",
        dest="ent",
        default=None,
        type=str,
        help="Entry to examine: prints out the SUBENTs",
    )
    parser.add_argument(
        "-f",
        dest="getFile",
        default=False,
        action="store_true",
        help="Don't use the exfor_manager.X4DBManager, just grab from the file directly.  The file name is constructed from the ENTRY you specify and resides in the main x4i database.",
    )
    parser.add_argument(
        "-c",
        dest="useCompressed",
        default=False,
        action="store_true",
        help="Use compressed dictionary instead of full file database.",
    )
    parser.add_argument(
        "--raw",
        default=False,
        dest="raw",
        action="store_true",
        help="Get raw EXFOR file, don't translate",
    )
    parser.add_argument(
        "--rawdata",
        default=False,
        dest="rawdata",
        action="store_true",
        help="Extract raw form of data in EXFOR data",
    )
    parser.add_argument(
        "--data",
        default=False,
        dest="data",
        action="store_true",
        help="Extract simple form of data in EXFOR data",
    )
    parser.add_argument(
        "--rawdoc",
        default=False,
        dest="rawdoc",
        action="store_true",
        help="Extract documentation from an EXFOR SUBENT",
    )
    parser.add_argument(
        "--doc",
        default=False,
        dest="doc",
        action="store_true",
        help="Interpreted documentation from an EXFOR SUBENT",
    )
    parser.add_argument(
        "--nada",
        default=False,
        dest="nada",
        action="store_true",
        help="Don't actually do anything with the SUBENT",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = process_args()
    if args.subent is None and args.ent is None:
        raise ValueError("No ENTRY or SUBENT specified")
    if args.subent is not None and len(args.subent) != 8:
        raise ValueError("SUBENT must have 8 characters")
    if args.ent is not None and len(args.ent) != 5:
        raise ValueError("ENTRY must have 5 characters")

    # Get the ENTRY/SUBENTRY requested
    if not args.getFile:
        if args.useCompressed:
            dbMgr = exfor_manager.X4DBManagerMemoryCached()
        else:
            dbMgr = exfor_manager.X4DBManagerPlainFS()
        if args.ent is not None:
            searchResult = dbMgr.retrieve(ENTRY=args.ent)
        else:
            searchResult = dbMgr.retrieve(SUBENT=args.subent)
    else:
        if args.ent is not None:
            theEntry = args.ent
        else:
            theEntry = args.subent[0:5]
        searchResult = {
            theEntry: exfor_entry.x4EntryFactory(theEntry, rawEntry=args.raw)
        }
        if args.subent is not None:  # must filter
            if args.raw:
                pass
            else:
                if args.subent not in searchResult[theEntry]:
                    raise KeyError("SUBENT " + args.subent + " not found!")
                for k in list(searchResult[theEntry].keys()):
                    if k.endswith("001") or k == args.subent:
                        continue
                    #                    print 'removing',k
                    del searchResult[theEntry][k]

    # Just print out the SUBENT keys
    if args.ent is not None:
        print("This ENTRY:      ", list(searchResult.keys())[0])
        for i in searchResult[list(searchResult.keys())[0]]:
            print("   ", i.split("\n")[0][0:22])

    # Examine a SUBENT
    if args.subent is not None:
        subent = searchResult
        keys = sorted(searchResult.keys())
        if not args.nada:
            if args.raw:
                print("\n\n")
                for k in keys:
                    print("\n".join(searchResult[k]))
            if args.rawdoc:
                print("\n\n")
                print(repr(searchResult[keys[0]][1]))
            if args.doc:
                print("\n\n")
                print(searchResult[keys[0]][1])
            if args.rawdata:
                if args.subent.endswith("001"):
                    raise ValueError(
                        "Documentation SUBENTs (those ending in '001') do not"
                        + "have DATA sections"
                    )
                print(10 * "-", "Raw Data", 10 * "-")
                print(searchResult[keys[-1]][args.subent]["DATA"])
                print(10 * "-", "Errors", 10 * "-")
                print(searchResult[keys[-1]].errors)
            if args.data:
                if args.subent.endswith("001"):
                    raise ValueError(
                        "Documentation SUBENTs (those ending in '001') do not "
                        + "have DATA sections"
                    )
                print(10 * "-", "Data", 10 * "-")
                print(searchResult[keys[-1]].getDataSets())
                print(10 * "-", "Errors", 10 * "-")
                print(searchResult[keys[-1]].errors)
