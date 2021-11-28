import math
import retrieval_utils as utils
from retrieval_utils import CTColors


class InvertedIndex:
	"""
	Inverted index object that store the processed documents.
	"""
	docs_dict: dict[str, list[str]] = {}  # dict[doc_id, preprocessed_tokens]
	term_dict: dict[str, list[str]] = {}  # dict[term, posting_list]

	def __init__(self, docs_path: str):
		# read and preprocess documents
		for k, v in utils.read_documents(docs_path).items():
			self.docs_dict[k] = utils.preprocess_str(v)[0]
		print(f"{CTColors.OKGREEN}Documents preprocessing completed{CTColors.ENDC}")

		# indexing:
		for d_id, doc_content in self.docs_dict.items():
			for token in doc_content:
				if token not in self.term_dict:
					# if term not found in term_dict, create new dict entry: [term, first_id]
					self.term_dict[token] = [d_id]
				elif d_id not in self.term_dict[token]:
					# if term found, append new doc id to the term
					self.term_dict[token].append(d_id)

	def get_raw_tf(self, word: str, doc_id: str) -> int:
		"""
		Returns the raw term frequency of specific word in a specified document.
		"""
		tf = 0
		for term in self.docs_dict[doc_id]:
			if word == term:
				tf += 1
		return tf

	def get_idf(self, word: str) -> float:
		"""
		Returns the idf of a specific word in the inverted index object.
		"""
		if word not in self.term_dict:
			return 0
		return math.log2(len(self.docs_dict) / len(self.term_dict[word]))

	def get_tfidf(self, word: str, doc_id: str) -> float:
		"""
		Returns the tf-idf value of a specific word with respect to the specific document.
		"""
		return self.get_raw_tf(word, doc_id) * self.get_idf(word)

	def get_doc_length(self, doc_id: str) -> float:
		"""
		Returns the documents length of a specific document.
		"""
		result = 0
		for term in self.docs_dict[doc_id]:
			result += self.get_tfidf(term, doc_id) ** 2
		return math.sqrt(result)

	def __repr__(self):
		return str(self)

	def __str__(self):
		tmp = "Documents:\n"
		for d_id in self.docs_dict:
			tmp += str(self.docs_dict[d_id]) + "; "
		tmp += "\nTerms:\n"
		for term in self.term_dict:
			tmp += term + str(self.term_dict[term]) + "; "
		return tmp
