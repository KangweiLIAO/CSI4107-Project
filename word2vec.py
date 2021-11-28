import gensim.downloader
import retrieval_utils as utils
from inverted_index import InvertedIndex
from gensim import corpora
from gensim.models import Word2Vec
from gensim.matutils import cossim


def train_w2v_model(train_data: dict[str, list[str]]) -> Word2Vec:
	train_data = [words for words in train_data.values()]
	# train a skip-gram model:
	sg_model = Word2Vec(sentences=train_data, vector_size=100, min_count=2, window=5, sg=1, workers=4)
	print('Vocabulary size:', len(sg_model.wv.index_to_key))
	return sg_model.wv


def similarity_scores(inv_index: InvertedIndex, queries, pretrained: bool = True):
	scores_dict: dict[str, float] = {}  # dict[doc_id, score]
	if pretrained:
		model = gensim.downloader.load('word2vec-google-news-300')
	else:
		model = train_w2v_model(inv_index.docs_dict)

	for q_id, q_raw in queries:
		q_terms = utils.preprocess_str(q_raw)
		for term in q_terms:
			q_terms = ''.join(q_terms).replace(term, model.wv.most_similar(term, topn=1)[0]).split()
			tmp_dict = corpora.Dictionary([doc for _, doc in inv_index.docs_dict.items()])
			new_query = tmp_dict.doc2bow(q_terms)
			print(model.wv.cosine_similarities(new_query, [tmp_dict.doc2bow(doc) for _, doc in inv_index.docs_dict.items()]))
			exit(1)
	return scores_dict
