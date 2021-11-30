import time
import multiprocessing
import retrieval_utils as utils
from inverted_index import InvertedIndex
from retrieval_utils import CTColors
from gensim.models.doc2vec import Doc2Vec, TaggedDocument


def train_d2v_model(docs_dict):
	print("Training Doc2Vec model... (~= s)")
	start_time = time.time()
	# Prepare training set
	train_set = [TaggedDocument(docs_dict[key], tags=[key]) for key in docs_dict]
	model = Doc2Vec(vector_size=100, dm=1, alpha=0.01, window=5, workers=multiprocessing.cpu_count(),
					epochs=30)
	model.build_vocab(train_set)
	model.train(train_set, epochs=model.epochs, total_examples=model.corpus_count)
	print(f"{CTColors.OKBLUE}Training completed in", str(time.time() - start_time)[:6], f"seconds.{CTColors.ENDC}")
	return model


def similarity_scores(index: InvertedIndex, queries: list[(str, list[str])], doc_per_query=1000):
	# Load Model
	model = train_d2v_model(index.pred_docs_dict)
	print("Calculating similarity scores with doc2vec...")
	start_time = time.time()
	# Predict
	results = {}
	for pair in queries:  # (q_id, raw_query)
		query = pair[1].split()
		inferred_vector = model.infer_vector(query, alpha=0.025, epochs=model.epochs+20)
		sims = model.dv.most_similar_cosmul(positive=[inferred_vector], topn=doc_per_query)  # return [(d_id,sim_score)]
		results[pair[0]] = [(tag, score) for tag, score in sims]
	print("Calculation and ranking completed in", str(time.time() - start_time)[:6], "seconds")
	return results
