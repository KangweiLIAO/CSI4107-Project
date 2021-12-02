import time
import numpy as np
import multiprocessing
import retrieval_utils as utils
from inverted_index import InvertedIndex
from gensim.models import Word2Vec
from retrieval_utils import CTColors


def train_w2v_model(train_data: dict[str, list[str]], sg=1) -> Word2Vec:
	"""
	Train a word2vec model based on the training data

	:param train_data:
	:param sg: 0 for CBOW, 1 for skip-gram [default=1]
	:return: Word2Vec model
	"""
	print("Training Word2Vec model...")
	start_time = time.time()
	train_data = [words for words in train_data.values()]
	# train a skip-gram model:
	model = Word2Vec(sentences=train_data, vector_size=300, alpha=0.1, min_count=2, window=5, sg=sg,
					 workers=multiprocessing.cpu_count(), epochs=30)
	print(f"{CTColors.OKBLUE}Trained Completed in " + str(time.time() - start_time)[:6] + f" seconds.{CTColors.ENDC}",
		  end=' ')
	print(f"{CTColors.OKBLUE}(Vocabulary size:" + str(len(model.wv.index_to_key)) + f"){CTColors.ENDC}")
	return model


def similarity_scores(inv_index: InvertedIndex, queries: list[(str, list[str])], topn=3, doc_per_query=1000):
	"""
	Train the word2vec model and do the query expansion. Finally return a ranked result for input queries on all documents
	in inv_index.

	:param inv_index: a inverted index object
	:param queries: raw queries with query ids
	:param topn: how many synonyms add to query [default=3]
	:param doc_per_query: maintain doc_per_query score records
	:return: dictionary containing the scores
	"""
	model = train_w2v_model(inv_index.pred_docs_dict).wv
	scores_dict: dict[str, list[(str, float)]] = {}  # dict[q_id, list[(d_id, score)]]
	print("Calculating similarity scores with expanded queries... (~= 50s)")
	start_time = time.time()
	for q_id, q_raw in queries:
		scores_dict[q_id] = []
		q_terms = utils.preprocess_str(q_raw)
		tmp = []
		# Query expansion:
		for term in q_terms:
			tmp += [pair[0] for pair in model.most_similar_cosmul(positive=term, topn=topn)]
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


def get_mean_vector(w2v_model, words):
	"""
	Calculate and return the mean vector of the words in given word2vec model.

	:param w2v_model: gensim word2vec model (.wv)
	:param words:
	:return: empty list or mean vector
	"""
	words = [word for word in words if word in w2v_model.key_to_index]  # remove out-of-vocabulary words
	if len(words) >= 1:
		return np.mean(w2v_model[words], axis=0)
	else:
		return []
