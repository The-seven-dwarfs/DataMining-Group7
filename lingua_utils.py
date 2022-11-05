from math import log, ceil
import shutil as shl
import pandas as pd
import numpy as np
from lingua import Language, LanguageDetectorBuilder
import multiprocessing as mp

def concurrent_language_model(dataset : pd.DataFrame, parallelism_level : int) -> pd.DataFrame:

	def process_function(datset_part_number : int, dataset_part : pd.DataFrame, return_queue : mp.Queue) -> pd.DataFrame:
		# from all language: all avaiable languages
		# with low accuracy: faster, without this it takes at least 1 second for every tweet (but even more if the text is long)
		# with preload language model: slower in building the model but faster in the prediction
		detector = LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().with_preloaded_language_models().build()
		dataset_part["tweet_lang"] = [(detector.detect_language_of(text)) for text in dataset_part["text"]]
		return_queue.put( (dataset_part, datset_part_number) )
		print("Process number", datset_part_number, "finished")


	num_process = parallelism_level
	process_list = []
	splitted_dataset = np.array_split(dataset, num_process)
	concurrent_queue = mp.Queue()
	
	for i in range(len(splitted_dataset)):
		process_list.append(mp.Process(target=process_function, args=( i, splitted_dataset[i] , concurrent_queue,  )))

	for i in process_list:
		i.start()

	splitted_dataset = []

	print("All", num_process, "processes runnig ...")
	
	for i in range(len(process_list)):
		print("Trying to collect", i + 1, "/", len(process_list), "of information")
		splitted_dataset.append(concurrent_queue.get(block=True))

	print("All computation retreived, merging spitted datasets")

	splitted_dataset.sort(key = lambda x : x[1])
	splitted_dataset = ( i for (i, _) in splitted_dataset)
	dataset = pd.concat(splitted_dataset)
	dataset.reset_index(drop=True, inplace=True)

	print("Merging completed")
	return dataset
