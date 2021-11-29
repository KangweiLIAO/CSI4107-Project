import time
import retrieval_utils as utils
from inverted_index import InvertedIndex
from gensim.models.doc2vec import Doc2Vec, TaggedDocument


def train_d2v_model(docs_dict):
	# Prepare training set
	train_set = [TaggedDocument(docs_dict[key], tags=[key]) for key in docs_dict]
	model = Doc2Vec(train_set, vector_size=200, dm=1, alpha=0.025, epochs=20, window=5, workers=4)
	return model


def similarity_scores(index: InvertedIndex, queries: list[(str, list[str])], topn=1000, doc_per_query=1000):
	print("Calculating similarity scores with doc2vec... (~= 20s)")
	start_time = time.time()
	# Load Model
	model = train_d2v_model(index.docs_dict)
	# Predict
	results = {}
	for pair in queries:  # (q_id, raw_query)
		preprocess_query = utils.preprocess_str(pair[1])
		inferred_vector = model.infer_vector(doc_words=preprocess_query, alpha=0.025, epochs=20)
		sims = model.dv.most_similar(positive=[inferred_vector], topn=topn)  # 10 most similar doc (d_id,sim_score)
		results[pair[0]] = [(tag, score) for tag, score in sims]
	print("Calculation and ranking completed in", str(time.time() - start_time)[:6], "seconds")
	return results
