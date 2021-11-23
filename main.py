import math
import os
import re
from inverted_index import InvertedIndex
from inverted_index import preprocess

RES_PATH = os.getcwd() + "\\res\\"
OUTPUT_PATH = os.getcwd() + "\\out\\"


class CTcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def read_queries(file_path: str) -> list[(str, list[str])]:
	qid = ''
	q_list = []
	try:
		q_file = open(file_path, encoding='utf-8')
		for line in q_file:
			if "<num>" in line:
				qid = re.sub("[^0-9]", "", line)  # extract query id from the line
			elif "<title>" in line:
				# extract raw query string and preprocess it
				q_list.append((qid, preprocess(line.replace("<title>", '').replace("</title>", ''))))
	except FileNotFoundError:
		print(f"{CTcolors.FAIL}Specified query file not found.{CTcolors.ENDC}")
	return q_list


def cos_scores(q_terms: list[str], inv_index: InvertedIndex):
	scores_dict: dict[str, float] = {}  # dict[doc_id, cos_score]
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
	q_length = math.sqrt(sum([x ** x for x in qtfidf_dict.values()]))  # document length of query
	# compute cosine score for each doc:
	for doc in inv_index.docs_dict.values():
		score = 0
		common_terms = list(set(doc.terms).intersection(q_terms))
		for term in common_terms:
			score += qtfidf_dict[term] * inv_index.get_tfidf(term, doc.id)
		score /= q_length * inv_index.get_doc_length(doc.id)
		scores_dict[doc.id] = score
	return scores_dict


def save_results(file_name: str, q_id: str, scores_list: (str, float)):
	file = open(file_name, 'a')
	rank = 1
	for doc_id, score in scores_list:
		file.write(f"{q_id} Q0 {doc_id} {rank} {score} Round1\n")
		rank += 1
	file.close()


if __name__ == '__main__':
	# "Small_queries.txt" and "Small_test_set.txt" can be used for fast testing
	result_filename = "Results.txt"
	# generate inverted index:
	index = InvertedIndex(RES_PATH + "topics_MB1-49.txt", RES_PATH + "StopWords.txt")
	queries = read_queries(RES_PATH + "topics_MB1-49.txt")  # read queries from a file

	# prepare for to save results:
	try:
		os.mkdir(OUTPUT_PATH)  # Try create '/out' directory
	except FileExistsError as e:
		pass  # ignore FileExistsError if '/out' directory exist
	try:
		open(OUTPUT_PATH + result_filename)
		print(f"{CTcolors.WARNING}Warning: [{result_filename}] detected in 'out\\' folder.{CTcolors.ENDC}")
		print(
			f"{CTcolors.WARNING}Do you want to delete it? (press enter to remove, other key to exit){CTcolors.ENDC}",
			end='')
		choice = input()  # catches input from keyboard
		if choice == '':
			os.remove(OUTPUT_PATH + result_filename)  # delete old result file in 'out/'
			print(
				f"{CTcolors.HEADER}Old [{result_filename}] removed, creating new [{result_filename}]...{CTcolors.ENDC}")
		else:
			print(f"{CTcolors.FAIL}Interrupted by user.{CTcolors.ENDC}")
			exit()  # exit program
	except FileNotFoundError as e:
		# if no old result file found in 'out/' folder:
		print(f"{CTcolors.HEADER}Start generating [{result_filename}] in 'out\\' folder.{CTcolors.ENDC}")

	# obtain cosine scores and save them to a result file:
	for qid, query in queries:
		scores = cos_scores(query, index)
		sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
		# for each query, save the 100 most relevant documents
		save_results(OUTPUT_PATH + result_filename, qid, sorted_scores[:100])
	print(f"{CTcolors.OKGREEN}Succeed: New [{result_filename}] created in 'out\\'.{CTcolors.ENDC}")
