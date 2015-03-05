[![Build Status](https://travis-ci.org/srnas/barnaba.svg)](https://travis-ci.org/srnas/barnaba)

INTRODUCTION
============
BaRNAba is a tool for analyzing RNA three-dimensional structures.
BaRNAba has been developed by Sandro Bottaro with the crucial help of Giovanni Bussi.
For bugs, questions or comments contact Sandro at sbottaro@sissa.it. 
If you use baRNAba in your work,  please cite the follwing paper:

S.Bottaro, F. di Palma, G.Bussi. The role of nucleobases 
in RNA structure and dynamics. 
Nucleic Acids Research (2014)

INSTALLATION
============
BaRNAba is distributed as a Python script. It requires
Python version 2.7 with Numpy and Scipy libraries.

You can obtain barnaba using git:

    git clone git://github.com/srnas/barnaba.git

or download a zip file from the web:

   https://github.com/srnas/barnaba


USAGE
=====

* minimal help
  ./baRNAba --help 

Currently, baRNAba can perform 5 different tasks:
1. Calculate the ERMSD between structures
   ./baRNAba ERMSD --pdb sample1.pdb -f sample2.pdb

2. Calculate the ESCORE
   ./baRNAba ESCORE --force-field 1S72.pdb -f sample1.pdb

3. Find hairpin loop motif
   ./baRNAba SS_MOTIF --query motif.pdb -f file1.pdb file2.pdb ... 

4. Find double stranded motif. l1 and l2 are the lengths of the two strands
   ./baRNAba DS_MOTIF --query motif.pdb -f file1.pdb file2.pdb ... --l1 l1 --l2 l2

5. Annotate structures/trajectories according to the Leontis/Westhof classification.  
   ./baRNAba ANNOTATE -f file1.pdb file2.pdb ...

practical examples can be found in the examples folder. 










