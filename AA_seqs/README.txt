Fas_to_csv.py

Takes a fasta file as input, and outputs a CSV file where for each sequence a new row is assigned. Each amino acid in a sequence is assigned to a single cell within a row. 

To use, change the file input directory, input file name, and output file name.  

Upon Completion, open the CSV file and insert headers for the accession number and amino acid position: [Accession][1][2][3][...] 


seq_match_branch.py

Takes the output of fas_to_csv and the output of downsize_branchify (Grouping information). It outputs a csv file where each sequence has a group identifier.
