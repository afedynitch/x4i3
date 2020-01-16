=========================
x4i - The EXFOR Interface
=========================

Date:   2/15/2011
Author: David Brown

Description: 
x4i provides a "simple" python interface to the EXFOR library, allowing users to 
search for and then translate EXFOR files into an easy to understand (and then plot) form.

Detailed instructions are provided in doc/x4i/x4i.pdf



Installation
============

Local Installation:
-------------------

1. Put x4i in your PYTHONPATH

2. There is no step 2

Site-wide Installation:
-----------------------

1. sudo python setup.py install 

2. There is no step 2



How do I get x4i?
=================

From the subversion repository on the OCF:
------------------------------------------

1. Check out the code:
        svn co svn+ssh://username@ocfmachine.llnl.gov/usr/gapps/CNP_src/all/live_repos/svnRepos/x4i/trunk/x4i
   You must be a member of the ndg group on LLNL's Open Computing Facility.
   
2. Unpack the EXFOR data contained in the svn repo:
        python x4i/setupEXFORdb.py -u

3. Follow the installation instructions above

From a tarball:
---------------

1. Unpack the tarball:
        tar xzf x4i-1.0.tar.gz
        
2. Follow installation instructions above


How do I import new EXFOR data?
===============================
The IAEA distributes zipfiles containing the entire EXFOR database, one entry per file.  x4i can be 
updated with the contents of this file.  Assuming you just downloaded the EXFOR file X4-2010-12-31.zip, 
do:
    python bin/x4i/setupEXFORdb.py -EXFOR-2013-05-30

Please read the help message (python setupEXFORdb.py -h) for more information.

