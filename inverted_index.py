import math
import re
import time
import retrieval_utils as utils
from retrieval_utils import CTColors


class TokenDoc:
	id: str
	terms: list[str]

	def __init__(self, doc_id: str, terms: list[str]):
		self.id = doc_id
		self.terms = terms

	def __len__(self):
		return len(self.terms)

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "TokenDoc{" + "docID='" + self.id + '\'' + ", terms=" + str(
			self.terms) + "}"


class InvertedIndex:
	docs_dict: dict[str, TokenDoc] = {}
	term_dict: dict[str, list[str]] = {}  # dict[term,list[docID]]

	def __init__(self, docs_path: str):
		raw_docs: list[str] = []
		try:
			doc_files = open(docs_path, encoding='utf-8')
			raw_docs = doc_files.readlines()
			doc_files.close()  # close the doc source file
			print(f"{CTColors.OKGREEN}Documents successfully read.{CTColors.ENDC}")
		except FileNotFoundError as e:
			print(f"{CTColors.FAIL}Documents file not found:{CTColors.ENDC}")
			print(e)

		start_time = time.time()
		print("Preprocessing documents...")
		for each in raw_docs:
			each = each.split("\t")  # split id and content
			each[0] = re.sub("[^0-9]", "", each[0])  # remove non-numerical char for doc id
			self.docs_dict[each[0]] = TokenDoc(each[0], utils.preprocess_str(each[1]))  # append to doc array
		print("Preprocessing end in", str(time.time() - start_time) + " seconds")

		# indexing:
		for doc in self.docs_dict.values():
			for token in doc.terms:
				if token not in self.term_dict.keys():
					# if term not found in term_dict, create new dict entry: (id, raw_tf)
					self.term_dict[token] = [doc.id]
				elif doc.id not in self.term_dict[token]:
					# if term found, append new doc id to the term
					self.term_dict[token].append(doc.id)

	def get_raw_tf(self, word: str, doc_id: str) -> int:
		tf = 0
		for term in self.docs_dict[doc_id].terms:
			if word == term:
				tf += 1
		return tf

	def get_idf(self, word: str) -> float:
		if word not in self.term_dict:
			return 0
		return math.log2(len(self.docs_dict) / len(self.term_dict[word]))

	def get_tfidf(self, word: str, doc_id: str) -> float:
		return self.get_raw_tf(word, doc_id) * self.get_idf(word)

	def get_doc_length(self, doc_id: str) -> float:
		result = 0
		for term in self.docs_dict[doc_id].terms:
			result += self.get_tfidf(term, doc_id) ** 2
		return math.sqrt(result)
