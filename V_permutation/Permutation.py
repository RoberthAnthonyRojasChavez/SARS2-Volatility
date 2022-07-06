import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



############## Neighbors ###############

def _missing_finder(missing_df, pos):
    """
    A helper function used in `neighbor_finder` function.
    """
    extra = []
    extra.extend(list(missing_df.loc[missing_df.pos1 == pos, 'pos2'].values))
    extra.extend(list(missing_df.loc[missing_df.pos2 == pos, 'pos1'].values))    
    if len(extra) != 0:
        extra_series = pd.Series([3.5 for n in range(len(extra))], index=extra)
        return extra_series
    else:
        return None
    




def _add_extra(main_df, pos, additional_neighbors):
    """
    A helper function used in `neighbor_finder` function.
    """
    return pd.concat([main_df[str(pos)], additional_neighbors], axis='rows', sort=False)





def neighbor_finder(main_df, missing_df, pos, n_neighbors=10):
    """
    Finds the closest neighbors to a position of interest `pos`

    Parameters
    ----------
    main_df: pd.DataFrame
        The distance dataframe
    missing_df: pd.DataFrame
        A dataframe with the of the missing pairs and their distances
    pos: int
        Position of interest
    n_neighbors: int
        Neighborhood size

    Return
    ------
    np.array: An array of size `n_neighbors` with the index of closest positions to position `pos`.
    """
    additional_neighbors = _missing_finder(missing_df, pos)
    if additional_neighbors is not None:
        final_series = _add_extra(main_df, pos, additional_neighbors)
    else:
        final_series = main_df[str(pos)].copy()
    final_series.drop(index=pos, inplace=True)
    return [*final_series.nsmallest(n_neighbors).index]







################# Permutation #################

def _find_statistic(df, reference_value, neighbors):
    """
	Finding the statistic value given the data

    Parameters
    ----------
    df: pd.Series, np.array
		A Series/array of volatility values (binary)
    reference_value: int
    	The volatility value for the position of interest that we want to calculate 
    	the sums of square regarding its neighbors.
    neighbors: list
    	List of indices for the closest neighbors
    """
    return (df.loc[neighbors].values*reference_value).sum()






def _permute(df, pos):
    """
	permutating
	"""
    # removing the position itself
    df_new = df.drop(index=pos).copy()
    # shuffling the dataframe
    df_new = df_new.sample(frac=1)
    # reindex the dataframe
    df_new.index = set(df.index).difference({pos})
    return df_new






def permutation_test(df, pos, dist_main, dist_missing, n_neighbors=10, N=1000, verbose=False, plot=False):
    """
    Implementation of Permutation test

	Parameters
	----------
	df: pd.Series, np.array
		A Series/array of volatility values (binary)
	pos: int
		Position of interest
	dist_main: pd.DataFrame
		Main distance matrix
	dist_missing: pd.DataFrame
		distance matrix of missing pairs
	n_neighbors: int
		Neighborhood size
	N: int 
		Number of permutations (default=1000)
	verbose: boolean
		Show the messages during implementations (default=False)
		Show neighbors indices and the value of null statistic.
	plot: boolean
		Show the histogram of the permutation results (default=False)
	
	Return
	------
	P-value of the test
	if `plot=True`: Histogram of the permutation results
	"""
    statistics_list = []
    neighbors = neighbor_finder(main_df=dist_main, 
                                missing_df=dist_missing, 
                                pos=pos, 
                                n_neighbors=n_neighbors)
    
    # the reference value to compare
    vp_at_pos = df.loc[pos]
    
    null_statistic = _find_statistic(df=df, reference_value=vp_at_pos, neighbors=neighbors)
    for i in range(N):
        permuted_df = _permute(df=df, pos=pos)
        statistics_list.append(_find_statistic(df=permuted_df, 
                                               reference_value=vp_at_pos, 
                                               neighbors=neighbors))
    
    permuted_statistics = np.array(statistics_list)
        
    if verbose:
        print('Neighbors:', neighbors)
        print('Null Statistic:', null_statistic)
        
    if plot:
        plt.hist(statistics_list, bins=np.arange(-0.5, n_neighbors+1.5, 1), edgecolor='grey', color='purple')
        plt.xticks(np.arange(1, n_neighbors+1, 1))
        plt.vlines(x=null_statistic, ymin=0, ymax=400, linestyle='dashed', color='green')
        plt.show()
    

    p_value = (permuted_statistics>=null_statistic).sum()/N
    
    return p_value




