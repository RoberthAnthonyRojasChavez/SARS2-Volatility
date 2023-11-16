Requirements:
Python 3.7
Java 16


The scripts were validated on Pycharm and IntelliJ IDEA in a macOS environment (Monterrey V 12.4). Running the code in a Windows environment (Tested on Windows 10 Enterprise 20H2) may result in formatting issues.
Instructions to run the code are found within each folder and within the code as comments.
Sample input|output datasets can be found here: https://drive.google.com/drive/folders/1qDimifO_S-1yp-pIfXydyw_2vkxTWF6B?usp=sharing

Installation time: No installation of our code is required.

Expected run time: Unless otherwise stated, code ran in a Windows 10 machine, i7-10700 @2.90gHZ, 60Gb RAM DDR4 3000 Mhz. Storage device: PCIe NVMe Gen3 3D NAND. Code runs in macOS ran in a MacbookAir M1 with 8Gb of RAM.

To obtain V, D and R metrics, run code in the following order (expected overall run time in parentheses):

	1. Tree (2 min)
	2. AA_seqs (2 min)
	3. V (2 min)
	4. D (5 min - in macOS)
	5. R (3 min)

Other Code:
	6. Lineage_permutation_MDS (20 min)
	7. V_permutation (5 min)

The code should be executed according to the order indicated:

1. Folder ID: Tree_Grouping: Code used for phylogenetic analyses.	
1.1. branchify.py: Branchify takes a newick tree file and outputs grouped sequence IDs based on the provided distance threshold.	
	Input: Tree_input_sample.txt	
	Output: Branchify_output_sample.txt
1.2. downsize_branchified_groups.py: This program takes a partitioned group txt file (output of the above) and divides the large groups (larger than the cutoff size of 50, designated the “ceiling”) into multiple smaller groups (e.g., 50 sequences per group). The code also removes the groups that are smaller than the cutoff number.	
	Input: Branchify_output_sample.txt	
	Output: Downsize_branchified_groups_output_sample.txt	

2. Folder ID:AA_seqs_group_attributes: The code takes grouping information from Tree_Grouping and a fasta file (aligned amino acids) and combines them into a .csv file where sequences are assigned their groups as determined above. 
2.1 fas_to_csv.py: Takes a fasta file as input and outputs .csv file where each residue is assigned a cell.	
               Input: Example_Fasta_file.fasta	
              Output: Example_output_csv_fas_to_csv.csv
2.2 seq_match_branch.py: Takes the output of fas_to_csv and the output of downsize_branchify.py (Grouping information). It outputs a csv file where each sequence has a group identifier.	
	Inputs: Example_output_csv_fas_to_csv.csv
                            Seq_match_branch_input_groups_50s.txt
	Output: Example_output_seq_match_branch.csv

3. Folder ID:V_metric: Code used to obtain the Volatility metric V.
3.1 stdev_cal.py: The code assigns each amino acid a value according to its hydropathy score. Each residue, including a PNGS, has a different value according to a modified Black and Mould score (built into the code). The standard deviation of the hydropathy scores across a cluster of 50 sequences is calculated.
	Input: stdev_cal_input.csv
	Output: sample_stdev_output.csv

4. Folder ID: R_metric: Code used to obtain the volatility metric R.
4.1 stdev_cal.py: Code calculates the standard deviation of the hydropathy scores across a cluster of 50 sequences. 
	Input: stdev_cal_input.csv
	Output: sample_stdev_output.csv
4.2 FisherExact.java: The code calculates the co-mutability of any two spike positions. The code uses as input a matrix that contains all spike positions (in columns) and all 50-sequence clusters (in rows). The values describe the absence (0) or presence (1) of volatility in each cluster at each position. The output is a matrix that contains the P-values in the tests.
	Input: test_stdev_fisher_input.csv
	Output: FisherExact_output.csv
4.3. fisherMatrix_to_Column.py: Code used to transform the above matrix into a column format and to filter out position pairs based on their values (position pairs with P-values smaller than a defined threshold are listed)
	Input: FisherExact_output.csv
	Output: R_metric_network_output.csv
4.4 R.py: Code computes the R metric from a log-transformed volatility input.
	Inputs: Sample_R_input.csv
                            fishermatrix_to_column_output_log_transformed.csv
	Output: sample_stdev_output.csv

5. Folder ID: D_metric: Code used to obtain the volatility metric D. 
5.1. Subfolder: Trimer Distance: The folder contains code used to calculate the minimal distance (in Å) between any two positions of spike.
5.1.1: trimer_eucli_distance.py: Code to calculate the above Euclidean distances. 
	Input: input for trimer_eucli_dist.csv
	Output: output_trimer_eucli_dist.csv
5.1.2: convert_to_pos_matrix.py: Code to obtain the shortest distance between any two positions and accounts for the three protomers of the protein. 
	Input: output_trimer_eucli_dist.csv
              Output: output_convert_to_post_matrix.csv
5.1.3: fisherMatrix_to_Column.py: Code used to transform the above matrix into a column format and to filter out position pairs with Euclidean distances above a user-defined threshold.
               Input: output_convert_to_post_matrix.csv
	Output: final_6zgi_output.csv
5.2 stdev_cal.py: Code calculates the standard deviation of the hydropathy scores across a cluster of 50 sequences.
	Input: stdev_cal_input.csv
	Output: sample_stdev_output.csv
5.3 D.py: Code calculates the metric D, which describes the total volatility at all positions within a given distance, which is weighted by the reciprocal of the distance.
	Inputs: input_for_D_6zgi_distances_reciprocal.csv
                            Sample_D_input.csv
              Output: sample_D_output.csv

6. Folder ID: Lineage_permutation_MDS: Code calculates the lineage specificity of n-feature vectors based on Euclidean distances between them and their lineage-association.
6.1 specificity.py
	Inputs: MDS_sample_input.csv
	Output: P-values are indicated in the Console.



7. Folder ID: V_permutation: Calculates the clustering of volatility on the spike trimer. 
7.1 implement.py: Invokes the permutation test from Permutation.py. The code applies values as inputs as well as a Euclidean distance matrix. The output is the P-value that indicates the presence of an environment that is more volatile than any randomly selected environment.
	Inputs: 10.27.21 Baseline_Vp.csv (Volatility Values)
		10.25.21 No_gaps.csv (Distance matrix)
		10.25.21 missing data.csv (Positions with no distance information, gaps in trimer structure)
	Output: List of Neighbors associated with the position of interest.
                              Null Statistic
                              P-value
	
