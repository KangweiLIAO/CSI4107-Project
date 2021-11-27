import gensim.downloader
from gensim.models import Word2Vec


def train_w2v_model(train_data: dict[str, list[str]]) -> Word2Vec:
	train_data = [words for words in train_data.values()]
	# train a skip-gram model:
	sg_model = Word2Vec(sentences=train_data, vector_size=100, min_count=2, window=5, sg=1,workers=4)
	print('Vocabulary size:', len(sg_model.wv.index_to_key))
	return sg_model


def similarity_scores(inv_index):
	scores_dict: dict[str, float] = {}  # dict[doc_id, score]

	return scores_dict
