from lingua import Language, LanguageDetectorBuilder
import multiprocessing as mp


def concurrent_language_model(dataset : pd.DataFrame) -> pd.DataFrame:

	def process_function(datset_part_number : int, dataset_part : pd.DataFrame, return_queue : mp.Queue) -> pd.DataFrame:
		# from all language: all avaiable languages
		# with low accuracy: faster, without this it takes at least 1 second for every tweet (but even more if the text is long)
		# with preload language model: slower in building the model but faster in the prediction
		detector = LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().with_preloaded_language_models().build()
		dataset_part["tweet_lang"] = [detector.detect_language_of(text) for text in dataset_part["text"]]
		return_queue.put( (dataset_part, datset_part_number) )

	num_process = 12
	process_list = []
	splitted_dataset = np.array_split(dataset, num_process)
	concurrent_queue = mp.Queue()
	
	
	for i in range(num_process):
		process_list.append(mp.Process(target=process_function, args=( i, splitted_dataset[i] , concurrent_queue,  )))
	
	for i in process_list:
		i.start()
	
	for i in process_list:
		i.join()

	
	splitted_dataset = []
	for i in range(num_process):
		splitted_dataset.append(concurrent_queue.get(block=False))

	splitted_dataset.sort(key = lambda x : x[1])
	splitted_dataset = ( i for (i, _) in splitted_dataset)
	dataset = pd.concat(splitted_dataset)
	dataset.reset_index(drop=True, inplace=True)
	return dataset