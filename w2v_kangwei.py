from gensim.models import Word2Vec


def train_w2v_model(train_data: dict[str, list[str]]) -> Word2Vec:
	train_data = [words for words in train_data.values()]
	model = Word2Vec(sentences=train_data, vector_size=100, min_count=2, window=5, sg=1, workers=4)
	print('Vocabulary size:', len(model.wv.index_to_key))
	print(model.wv.most_similar('BBC', topn=10))
	return model


def embedding_w2v(tokens):
	pass


def similarity_scores():
	pass
