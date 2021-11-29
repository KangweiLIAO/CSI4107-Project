import time
import math
import retrieval_utils as utils
from inverted_index import InvertedIndex


def similarity_scores(inv_index: InvertedIndex, queries):
	start_time = time.time()
	scores_dict: dict[str, list[(str, float)]] = {}  # dict[q_id, list[(d_id, score)]]
	for q_id, q_raw in queries:
		scores_dict[q_id] = []
		q_terms = utils.preprocess_str(q_raw)  # preprocessing query
		qtf_dict: dict[str, int] = {}  # dict[q_term, tf]
		qtfidf_dict: dict[str, float] = {}  # dict[q_term, tfidf]

		# compute raw tf of q_terms:
		for term in q_terms:
			term = term.lower()
			if term not in qtf_dict.keys():
				qtf_dict[term] = 1
			else:
				qtf_dict[term] += 1

		# compute tf-idf of q_terms:
		for term in q_terms:
			term = term.lower()
			qtfidf_dict[term] = qtf_dict[term] * inv_index.get_idf(term)
		q_length = math.sqrt(sum([x ** 2 for x in qtfidf_dict.values()]))  # compute length of query vector

		# compute cosine similarity between the query and all docs:
		for d_id, d_words in inv_index.docs_dict.items():
			score = 0
			common_terms = list(set(d_words).intersection(q_terms))
			for term in common_terms:
				term = term.lower()
				score += qtfidf_dict[term] * inv_index.get_tfidf(term, d_id)
			doc_length = inv_index.get_doc_length(d_id)
			if not (q_length == 0 or doc_length == 0):
				# If document length == 0 (all words in the document been identified as stopwords) or empty query
				score /= q_length * inv_index.get_doc_length(d_id)
			scores_dict[q_id].append((d_id, score))
		sorted_scores = sorted(scores_dict[q_id], key=lambda item: item[1], reverse=True)
		scores_dict[q_id] = sorted_scores
	print("Calculation and ranking completed in", str(time.time() - start_time)[:6], "seconds")
	return scores_dict
