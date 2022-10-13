from math import log, ceil
from datetime import datetime
import shutil as shl

import pandas

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

def unpack():
	shl.unpack_archive("dataset/users.zip", "dataset") # unpacks the users.zip into the datasets folder (The users zip is small enough to be commited to github if we would like)
	shl.unpack_archive("dataset/tweets.zip", "dataset") # unpacks the tweets.zip into the datasets folder

def repair_lang_attribute(users_df: pandas.DataFrame):
	wrong_fields = ["Select Language...", "xx-lc"] # only 3 elements
	to_map_fields = {
		"en-gb": "en-GB",
		"zh-tw": "zh-TW",
		"zh-cn": "zh-CN",
		"fil": "fil-PH"
	}

	# dropping wrong fields
	wrong_index = lambda x: True if x[1] in wrong_fields else False
	wrong_indexes = [index for (index, _) in filter(wrong_index, enumerate(users_df["lang"]))]
	#users_df.drop(index=wrong_indexes, inplace=True)

	# mapping incorrect values to fixed ones
	for language in to_map_fields:
		indexes = users_df[users_df["lang"] == language].index
		for index in indexes:
			old_language = users_df.loc[index,"lang"]
			users_df.loc[index,"lang"] = to_map_fields[old_language]