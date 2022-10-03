from math import log, ceil

def get_sturges_bins(sample_size: int)->float:
	"""
	Given the sample size of a distribution, returns the number of bins 
	for an histogram rapresenting the distribution according to Sturges' rule 
	"""
	return ceil( log(sample_size,2) + 1 )
