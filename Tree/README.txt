Branchify takes a newick tree file and outputs grouped sequence IDs based on the provided distance threshold. 

To run branchify, you must provide the following parameters:
-i is the input directory.
-m is the file type (newick)
-t is the distance threshold
-o is the output directory.

	example:

	-i
	C:\Users\rojaschavez\Desktop\2\C.37_branchify_ready.txt  
	-m
	newick
	-t
	0.004
	-o
	C:\Users\rojaschavez\Desktop\2\C.37_branchify_ready_0.004.txt


downsize_branchified_groups:
This program takes a branchified groups txt file. ad divides the groups larger than the cutoff (ceiling) into multiple smaller groups (50 sequences per group). It also removes the groups that are smaller than the cutoff number.
