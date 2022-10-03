from math import log, ceil
from datetime import datetime

def is_datetime_format_correct(date_string: str, expected_format: str)->bool:
	"""
	Checks if the string date_string is representing a datetime in the format
	expressed by expected_format
	"""
	try:
		datetime.strptime(date_string, expected_format)
		return True
	except ValueError:
		return False

def get_sturges_bins(sample_size: int)->float:
	"""
	Given the sample size of a distribution, returns the number of bins 
	for an histogram rapresenting the distribution according to Sturges' rule 
	"""
	return ceil( log(sample_size,2) + 1 )
