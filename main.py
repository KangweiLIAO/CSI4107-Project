import math
import os
import retrieval_utils as utils
from inverted_index import InvertedIndex
from inverted_index import CTColors

RES_PATH = os.getcwd() + "/res/"
OUTPUT_PATH = os.getcwd() + "/out/"
N_MOST_DOC = 1000


def similarity_score(q_terms: list[str], inv_index: InvertedIndex, pattern: str = ''):
	"""
	Returns a dictionary (dict[doc_id, score]) containing the similarity scores for a given query

	:param q_terms: a tokenized query
	:param inv_index: inverted index containing the documents
	:param pattern: algorithm used to obtain similarity scores (cosine, word2vec)
	:return: a dictionary containing the similarity scores for all documents in the inverted index
	"""
	scores_dict: dict[str, float] = {}  # dict[doc_id, score]
	if pattern == 'cosine' or pattern == '':
		qtf_dict: dict[str, int] = {}
		qtfidf_dict: dict[str, float] = {}
		# compute raw tf of q_terms:
		for term in q_terms:
			if term not in qtf_dict.keys():
				qtf_dict[term] = 1
			else:
				qtf_dict[term] += 1
		# compute tf-idf of q_terms:
		for term in q_terms:
			qtfidf_dict[term] = qtf_dict[term] * inv_index.get_idf(term)
		q_length = math.sqrt(sum([x ** 2 for x in qtfidf_dict.values()]))  # document length of query
		# compute cosine score for each doc:
		for doc in inv_index.docs_dict.values():
			score = 0
			common_terms = list(set(doc.terms).intersection(q_terms))
			for term in common_terms:
				score += qtfidf_dict[term] * inv_index.get_tfidf(term, doc.id)
			doc_length = inv_index.get_doc_length(doc.id)
			if not (q_length == 0 or doc_length == 0):
				# If document length == 0 (all words in the document been identified as stopwords) or empty query
				score /= q_length * inv_index.get_doc_length(doc.id)
			scores_dict[doc.id] = score
	elif pattern == 'word2vec':
		pass
	return scores_dict


if __name__ == '__main__':
	# "Small_queries.txt" and "Small_test_set.txt" can be used for fast testing
	result_filename = "Results.txt"
	# add custom stopwords:
	utils.add_stopwords(RES_PATH + "StopWords.txt")
	# generate inverted index:
	index = InvertedIndex(RES_PATH + "Trec_microblog11.txt")
	queries = utils.read_queries(RES_PATH + "topics_MB1-49.txt")  # read queries from a file

	# prepare for to save results:
	try:
		os.mkdir(OUTPUT_PATH)  # Try create '/out' directory
	except FileExistsError as e:
		pass  # ignore FileExistsError, if '/out' directory exist
	try:
		open(OUTPUT_PATH + result_filename)  # detect result file
		print(
			f"{CTColors.WARNING}Warning: [{result_filename}] detected in 'out\\' folder.{CTColors.ENDC}")
		print(
			f"{CTColors.WARNING}Do you want to delete it? (press enter to remove, other key to exit){CTColors.ENDC}",
			end='')
		choice = input()  # catches input from keyboard
		if choice == '':
			os.remove(OUTPUT_PATH + result_filename)  # delete old result file in 'out/'
			print(
				f"{CTColors.HEADER}Old [{result_filename}] removed, creating new [{result_filename}]...{CTColors.ENDC}")
		else:
			print(f"{CTColors.FAIL}Interrupted by user.{CTColors.ENDC}")
			exit()  # exit program
	except FileNotFoundError as e:
		# if no old result file found in 'out/' folder:
		print(
			f"{CTColors.HEADER}Start generating [{result_filename}] in 'out\\' folder.{CTColors.ENDC}")

	# obtain cosine scores and save them to a result file:
	for qid, query in queries:
		scores = similarity_score(query, index)
		# Sort the similarity scores dictionary
		sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
		# for each query, save the N_MOST_DOC most relevant documents
		utils.save_results(OUTPUT_PATH + result_filename, qid, sorted_scores[:N_MOST_DOC])
	print(f"{CTColors.OKGREEN}Succeed: New [{result_filename}] created in 'out\\'.{CTColors.ENDC}")
