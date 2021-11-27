import re
import spacy

nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser'])


class CTColors:
	"""
	Colors for console texts.
	"""
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def add_stopwords(stopwords_path: str):
	"""
	Add custom stopwords from specified file to language model.

	:param stopwords_path: path to stopwords file
	"""
	try:
		custom_stopwords = open(stopwords_path, encoding='utf-8').readlines()
		# add to nlp default stopwords:
		nlp.Defaults.stop_words |= set([w.replace('\n', '') for w in set(custom_stopwords)])
	except FileNotFoundError as e:
		print(
			f"{CTColors.FAIL}Fail to add custom stop words, since specified stopwords file not found:{CTColors.ENDC}"
		)
		print(e)


def preprocess_str(raw_str: str, s_type: str = 'doc'):
	"""
	Return the preprocessed string. Will not remove stopwords if s_type is 'query'.

	:param raw_str: raw string read from the file
	:param s_type: either 'doc' or 'query', 'doc' in default
	:return: preprocessed string, (and spacy NLP object if input is a query)
	"""
	raw_str = raw_str.replace('\n', '').strip()  # format string
	str_nlp = nlp(raw_str)  # tokenization
	if not s_type == "query":
		# if not passed in a query, do stopwords removal and lemmatization:
		return [w.lemma_.lower() for w in str_nlp if not (w.is_stop or w.like_url or w.like_num)]
	return [w.text for w in str_nlp if not (w.is_space or w.is_punct)], str_nlp


def read_documents(file_path: str):
	docs_dict = {}
	doc_files = open(file_path, encoding='utf-8')
	raw_docs = doc_files.readlines()
	for each in raw_docs:
		each = each.split("\t")  # split id and content
		each[0] = re.sub("[^0-9]", "", each[0])  # remove non-numerical char for doc id
		docs_dict[each[0]] = preprocess_str(each[1])  # append to doc dictionary:
	doc_files.close()
	return docs_dict


def read_queries(file_path: str) -> list[(str, list[str])]:
	"""
	Read raw queries from specified file.

	:param file_path: path to the query file
	:return: a list of queries [query_id, query_content]
	"""
	q_id = ''
	q_list: list[(str, list[str])] = []  # [(query_id, query_content)]
	try:
		q_file = open(file_path, encoding='utf-8')
		for line in q_file:
			if "<num>" in line:
				q_id = str(int(re.sub("[^0-9]", '', line)))  # extract query id from the line
			elif "<title>" in line:
				# extract raw query string and preprocess it
				q_list.append((q_id, line.replace("<title>", '').replace("</title>", '')))
		print(f"{CTColors.OKGREEN}Queries successfully read.{CTColors.ENDC}")
	except FileNotFoundError:
		print(f"{CTColors.FAIL}Specified query file not found.{CTColors.ENDC}")
	return q_list


def save_result(file_name: str, q_id: str, scores_list: (str, float)):
	"""
	Save ranking results for one query in the TREC result file format.

	:param q_id: the query ID
	:param file_name: file name for the result file
	:param scores_list: similarity scores list
	"""
	file = open(file_name, 'a')
	rank = 1
	for doc_id, score in scores_list:
		file.write(f"{q_id} Q0 {doc_id} {rank} {score} Round1\n")
		rank += 1
	file.close()
