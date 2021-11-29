import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import retrieval_utils as utils

RES_PATH = os.getcwd() + "/res/"
DOC_FILENAME = "Trec_microblog11.txt"


def train_d2v_model(dic):
	# Prepare training set
	train_set = []
	for key in dic:
		document = TaggedDocument(dic[key], tags=[key])
		train_set.append(document)

	print(train_set[0])

	# Train model
	model = Doc2Vec(train_set, min_count=2, window=3, vector_size=100, sample=1e-3, workers=4)
	model.build_vocab(train_set)
	model.train(train_set, total_examples=model.corpus_count, epochs=10)
	return model


def similarity_scores(dic, queries):
	# Load Model
	model = train_d2v_model(dic)
	# Predict
	results = {}
	for pair in queries:
		preprocess_query = utils.preprocess_str(pair[1])
		print(preprocess_query)
		inferred_vector = model.infer_vector(doc_words=preprocess_query, epochs=20)
		# sims = (id,score) 10 tuples
		sims = model.docvecs.most_similar([inferred_vector], topn=10)  # 10 most similar message
		values = results[pair[0]] = []
		for tag, score in sims:
			values.append((tag, score))
	print("query is ", queries[0][1])
	print(results[queries[0][0]])
	return results
