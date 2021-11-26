import math
from inverted_index import InvertedIndex


def similarity_scores(inv_index: InvertedIndex, q_terms: list[str]):
	scores_dict: dict[str, float] = {}  # dict[doc_id, score]
	qtf_dict: dict[str, int] = {}
	qtfidf_dict: dict[str, float] = {}

	# compute raw tf of q_terms:
	for term in q_terms:
		term = term.lower()
		if term not in qtf_dict.keys():
			qtf_dict[term] = 1
		else:
			qtf_dict[term] += 1

	# compute tf-idf vector of q_terms:
	for term in q_terms:
		term = term.lower()
		qtfidf_dict[term] = qtf_dict[term] * inv_index.get_idf(term)
	q_length = math.sqrt(sum([x ** 2 for x in qtfidf_dict.values()]))  # compute length of query vector

	# compute cosine score for each doc:
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
		scores_dict[d_id] = score
	return scores_dict
