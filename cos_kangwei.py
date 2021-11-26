import math
from inverted_index import InvertedIndex


def similarity_scores(inv_index: InvertedIndex, q_terms: list[str]):
	scores_dict: dict[str, float] = {}  # dict[doc_id, score]
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
	return scores_dict
