from Permutation import permutation_test
import pandas as pd


pos = int(input('Enter Position of Interest: '))
n_neighbors = int(input('Enter Neighborhood Size: '))
N = int(input('Enter the Number of Permutations: '))




if __name__ == "__main__":
	
	# Read Data Files
	data = pd.read_csv('Data/10.27.21 Baseline_Vp.csv', index_col=0)['vol']
	data = data.apply(lambda x: 1 if x>0 else 0)
	dist = pd.read_csv('Data/10.25.21 No_gaps.csv', index_col=0)
	missing = pd.read_csv('Data/10.25.21 missing data.csv', header=None, names=['pos1', 'pos2', 'dist'])


	A = permutation_test(df=data, 
	    	             pos=pos, 
	        	         dist_main=dist, 
	            	     dist_missing=missing, 
	                	 n_neighbors=n_neighbors, 
	                 	N=N,
	                 	verbose=True,
	                 	plot=True)

	print(f'p-value: {A}')