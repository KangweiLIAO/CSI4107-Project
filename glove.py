import time
import numpy as np
import retrieval_utils as utils
import gensim.downloader as api
from ir_index import IRIndex

pmodel = api.load("glove-twitter-200")


# comment if want use annother model
# pmodel = gensim.models.KeyedVectors.load_word2vec_format("glove.840B.300d.txt",binary=False)
# uncomment if want use 5gb model
# pmodel = gensim.models.KeyedVectors.load_word2vec_format("vectors.txt",binary=False)
# uncomment if want use the model we trained by our dataset


def output(train_data: dict[str, list[str]]):
	"""
	use the inverted index output a dataset for glove

	:param train_data: a inverted index object
	:return:
	"""
	data = open("F:\data.txt", 'w+', encoding='UTF-16')
	train_data = [words for words in train_data.values()]
	for i in range(len(train_data)):
		s = ""
		for j in range(len(train_data[i])):
			s = s + train_data[i][j] + " "
		print(s, file=data)


def similarity_scores(inv_index: IRIndex, queries: list[(str, list[str])], topn=1, doc_per_query=1000):
	"""
	Use the pre-trained glove model and do the query expansion. Finally return a ranked result for input queries on all documents
	in ir_index.

	:param inv_index: a inverted index object
	:param queries: raw queries with query ids
	:param topn: how many synonyms add to query [default=3]
	:param doc_per_query: maintain doc_per_query score records
	:return:
	"""
	start_time = time.time()
	model = pmodel
	scores_dict: dict[str, list[(str, float)]] = {}  # dict[q_id, list[(d_id, score)]]
	print("Calculating similarity scores with expanded queries... (~= 50s)")
	for q_id, q_raw in queries:
		scores_dict[q_id] = []
		q_terms = utils.preprocess_str(q_raw)
		tmp = []

		# Query expansion:
		for term in q_terms:
			tmp += [pair[0] for pair in model.most_similar(term, topn=topn)]
			tmp.append(term)
		q_terms += tmp

		q_vec = get_mean_vector(model, q_terms)
		for d_id, doc in inv_index.pred_docs_dict.items():
			doc_avg_vec = get_mean_vector(model, doc)
			if len(doc_avg_vec) > 0:
				scores_dict[q_id].append((d_id, utils.np_cossim(q_vec, doc_avg_vec)))
			else:
				scores_dict[q_id].append((d_id, 0))
		scores_dict[q_id] = sorted(scores_dict[q_id], key=lambda item: item[1], reverse=True)[:doc_per_query]
	print("Calculation and ranking completed in", str(time.time() - start_time)[:6], "seconds")
	return scores_dict


def get_mean_vector(glv_model, words):
	"""
	Calculate and return the mean vector of the words in given glove model.

	:param glv_model: trained glove model
	:param words:
	:return:
	"""
	words = [word for word in words if word in glv_model.key_to_index]  # remove out-of-vocabulary words
	if len(words) >= 1:
		return np.mean(glv_model[words], axis=0)
	else:
		return []
