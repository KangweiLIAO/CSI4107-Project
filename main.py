import os
import time
import retrieval_utils as utils
import doc2vec as d2v_algo
import word2vec as w2v_algo
import tfidf as tfidf_algo
from inverted_index import InvertedIndex
from inverted_index import CTColors

RES_PATH = os.getcwd() + "/res/"
OUTPUT_PATH = os.getcwd() + "/out/"

DOC_FILENAME = "Trec_microblog11.txt"  # Small_docset.txt or Trec_microblog11.txt
QUERIES_FILENAME = "topics_MB1-49.txt"  # Small_queries.txt or topics_MB1-49.txt
RESULT_FILENAME = "Results.txt"

N_MOST_DOC = 1000  # return n most relevant documents for each query


def rank_and_save(inv_index: InvertedIndex, model: str = 'w2v'):
	"""
	Read queries from file, obtain the scores and save the ranking.

	:param inv_index: inverted index containing the documents
	:param model: algorithm used to obtain similarity scores (cosine[default], word2vec)
	"""

	# read queries from a file:
	queries: list[(str, list[str])] = utils.read_queries(RES_PATH + QUERIES_FILENAME)
	# Applying models
	if model == 'tfidf':
		print("Calculating TF-IDF vectors...")
		result = tfidf_algo.similarity_scores(inv_index, queries)
	elif model == 'w2v':
		print("Training Word2Vec model...")
		result = w2v_algo.similarity_scores(inv_index, queries)
	elif model == 'd2v':
		print("Training Doc2Vec model...")
		result = d2v_algo.similarity_scores(inv_index, queries)
	else:
		result = None  # dict[doc_id, score]

	# prepare to save the results:
	try:
		os.mkdir(OUTPUT_PATH)  # Try create '/out' directory
	except FileExistsError as e:
		pass  # ignore FileExistsError, if '/out' directory exist
	try:
		open(OUTPUT_PATH + RESULT_FILENAME)  # detect result file
		print(
			f"{CTColors.WARNING}Warning: [{RESULT_FILENAME}] detected in 'out/' folder.{CTColors.ENDC}")
		print(
			f"{CTColors.WARNING}Do you want to delete it? (press enter to remove, other key to exit){CTColors.ENDC}",
			end='')
		choice = input()  # catches input from keyboard
		if choice == '':
			os.remove(OUTPUT_PATH + RESULT_FILENAME)  # delete old result file in 'out/'
			print(
				f"{CTColors.HEADER}Old [{RESULT_FILENAME}] removed, creating new [{RESULT_FILENAME}]...{CTColors.ENDC}")
		else:
			print(f"{CTColors.FAIL}Interrupted by user.{CTColors.ENDC}")
			exit()  # exit program
	except FileNotFoundError as e:
		# if no old result file found in 'out/' folder:
		print(f"Generating [{RESULT_FILENAME}] in 'out/' folder...")
	if result is not None:
		utils.save_results(OUTPUT_PATH + RESULT_FILENAME, result, N_MOST_DOC)


if __name__ == '__main__':
	# add custom stopwords:
	utils.add_stopwords(RES_PATH + "StopWords.txt")

	# generate inverted index:
	start_time = time.time()
	print("Preparing inverted index... (~= 100 seconds if no config file (.ii) provided)")
	index = InvertedIndex(RES_PATH + DOC_FILENAME, RES_PATH + "inverted_index.ii")
	print("Indexing completed in", str(time.time() - start_time)[:8] + " seconds")

	# obtain cosine scores and save them to a result file:
	rank_and_save(index)
	print(f"{CTColors.OKGREEN}Succeed: New [{RESULT_FILENAME}] created in 'out/'.{CTColors.ENDC}")
