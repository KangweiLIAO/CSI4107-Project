import os
import time
import retrieval_utils as utils
import w2v_kangwei as w2v_algo
import tfidf_kangwei as cos_algo
from inverted_index import InvertedIndex
from inverted_index import CTColors

RES_PATH = os.getcwd() + "/res/"
OUTPUT_PATH = os.getcwd() + "/out/"

DOC_FILENAME = "Trec_microblog11.txt"  # Small_docset.txt or Trec_microblog11.txt
QUERIES_FILENAME = "topics_MB1-49.txt"  # Small_queries.txt or topics_MB1-49.txt
RESULT_FILENAME = "Results.txt"

N_MOST_DOC = 1000  # return n most relevant documents for each query


def rank_and_save(inv_index: InvertedIndex, pattern: str = 'tfidf'):
	"""
	Read queries from file, obtain the scores and save the ranking.

	:param inv_index: inverted index containing the documents
	:param pattern: algorithm used to obtain similarity scores (cosine[default], word2vec)
	"""
	# read queries from a file:
	queries = utils.read_queries(RES_PATH + QUERIES_FILENAME)
	if pattern == 'tfidf':
		print("Calculating TF-IDF vectors...")
	elif pattern == 'w2v':
		print("Training Word2Vec model...")
	if pattern == 'tfidf':
		for qid, query in queries:
			q_terms = utils.preprocess_str(query)  # preprocessing query
			tmp_scores = cos_algo.similarity_scores(inv_index, q_terms)  # dict[doc_id, score]
			# Sort the dictionary by score and return a list of sorted doc_id:
			sorted_scores = sorted(tmp_scores.items(), key=lambda item: item[1], reverse=True)
			utils.save_result(OUTPUT_PATH + RESULT_FILENAME, qid, sorted_scores[:N_MOST_DOC])
	elif pattern == 'w2v':
		w2v_algo.train_w2v_model(inv_index.docs_dict)
		tmp_scores = w2v_algo.similarity_scores(inv_index, queries)


if __name__ == '__main__':
	# add custom stopwords:
	utils.add_stopwords(RES_PATH + "StopWords.txt")

	# generate inverted index:
	start_time = time.time()
	print("Preparing inverted index...")
	index = InvertedIndex(RES_PATH + DOC_FILENAME)
	print("Indexing completed in", str(time.time() - start_time) + " seconds")

	# prepare for to save results:
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
		print(
			f"Generating [{RESULT_FILENAME}] in 'out/' folder...")

	# obtain cosine scores and save them to a result file:
	start_time = time.time()
	rank_and_save(index)
	# for each query, save the N_MOST_DOC most relevant documents
	print("Calculation and ranking completed in", str(time.time() - start_time), "seconds")
	print(f"{CTColors.OKGREEN}Succeed: New [{RESULT_FILENAME}] created in 'out/'.{CTColors.ENDC}")
