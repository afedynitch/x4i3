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

import os
from distutils.core import setup

setup( 
    name = 'x4i3',
    version = '1.1.0',
    author = 'David A. Brown (x4i3: Anatoli Fedynitch)',
    author_email = 'dbrown@bnl.gov',
    maintainer='Anatoli Fedynitch',
    maintainer_email='afedynitch@gmail.com',
    license='GPLv2',
    packages = [ 'x4i3', 'x4i3.test', 'x4i3.graphs' ],
    package_dir={
        'MCEq': 'MCEq',
        'MCEq.geometry': 'MCEq/geometry',
        'MCEq.geometry.nrlmsise00': 'MCEq/geometry/nrlmsise00',
        'MCEq.geometry.corsikaatm': 'MCEq/geometry/corsikaatm'
    },
    package_data = { 
        'x4i3': [ 
            os.path.join( [ 'dicts', '*.txt' ] ), 
            os.path.join( [ 'data', '*.t*' ] ), 
            os.path.join( [ 'data', '*.pickle' ] ), 
            os.path.join( [ 'data', 'db', '*', '*.x4' ] ) ], 
        'x4i3.test': [ 
            '*.x4',
            os.path.join( [ 'data', 'test_data.tar.gz' ] ) ] }, 
    url = 'https://github.com/afedynitch/x4i3/',
    install_requires=[
        'six',
        'tqdm',
        'requests',
        'pyparsing',
        'networkx'
    ],
    requires=[
        'pyparsing'
    ],
    license = open( 'LICENSE.txt' ).read(),
    description = 'A "simple" python interface to the EXFOR library',
    long_description = open( 'README.txt' ).read(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Physics',
        'Intended Audience :: Science/Research',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)'
    ]
)
