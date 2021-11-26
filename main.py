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


def ranking_scores(inv_index: InvertedIndex, q_terms: list[str], pattern: str = 'w2v'):
	"""
	Returns a list of doc_id sorted by their scores corresponding to given query.

	:param q_terms: a tokenized query
	:param inv_index: inverted index containing the documents
	:param pattern: algorithm used to obtain similarity scores (cosine[default], word2vec)
	:return: a list of doc_id sorted by their scores corresponding to given query
	"""
	tmp_scores: dict[str, float] = {}  # dict[doc_id, score]
	if pattern == 'tfidf':
		tmp_scores = cos_algo.similarity_scores(inv_index, q_terms)
	elif pattern == 'w2v':
		w2v_algo.train_w2v_model(inv_index.docs_dict)
		print(f"{CTColors.OKBLUE}word2vec model trained on documents")
		tmp_scores = w2v_algo.similarity_scores()
	# Sort the dictionary by score and return a list of sorted doc_id:
	return sorted(tmp_scores.items(), key=lambda item: item[1], reverse=True)


if __name__ == '__main__':
	# add custom stopwords:
	utils.add_stopwords(RES_PATH + "StopWords.txt")

	# generate inverted index:
	start_time = time.time()
	print("Preparing inverted index...")
	index = InvertedIndex(RES_PATH + DOC_FILENAME)
	print("Indexing completed in", str(time.time() - start_time) + " seconds")
	# read queries from a file:
	queries = utils.read_queries(RES_PATH + QUERIES_FILENAME)

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
			f"{CTColors.HEADER}Start generating [{RESULT_FILENAME}] in 'out/' folder.{CTColors.ENDC}")

	# obtain cosine scores and save them to a result file:
	start_time = time.time()
	print("Calculating similarity scores...")
	for qid, query in queries:
		scores = ranking_scores(index, query)
		# for each query, save the N_MOST_DOC most relevant documents
		utils.save_results(OUTPUT_PATH + RESULT_FILENAME, qid, scores[:N_MOST_DOC])
	print("Calculation completed in", str(time.time() - start_time), "seconds")
	print(f"{CTColors.OKGREEN}Succeed: New [{RESULT_FILENAME}] created in 'out/'.{CTColors.ENDC}")
