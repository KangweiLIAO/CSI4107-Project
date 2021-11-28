import retrieval_utils as utils
from inverted_index import InvertedIndex
from gensim import corpora
from gensim.models import Word2Vec
from gensim.matutils import cossim
from retrieval_utils import CTColors


def train_w2v_model(train_data: dict[str, list[str]]) -> Word2Vec:
	train_data = [words for words in train_data.values()]
	# train a skip-gram model:
	sg_model = Word2Vec(sentences=train_data, vector_size=300, alpha=0.08, min_count=2, window=5, sg=1, workers=4)
	print(f'{CTColors.OKBLUE}Trained Completed - Vocabulary size:' + str(
		len(sg_model.wv.index_to_key)) + f"{CTColors.ENDC}")
	return sg_model


def similarity_scores(inv_index: InvertedIndex, queries, topn=3):
	model = train_w2v_model(inv_index.docs_dict)
	scores_dict: dict[str, list[(str, float)]] = {}  # dict[q_id, list[(d_id, score)]]
	tmp_dict = corpora.Dictionary([doc for _, doc in inv_index.docs_dict.items()])
	print("Calculating similarity scores with expanded queries...")
	for q_id, q_raw in queries:
		scores_dict[q_id] = []
		q_terms = utils.preprocess_str(q_raw)[0]
		tmp = []
		for term in q_terms:
			tmp += [pair[0] for pair in model.wv.most_similar(term, topn=topn)]
		q_terms += tmp
		new_query_bow = tmp_dict.doc2bow(q_terms)
		for d_id, doc in inv_index.docs_dict.items():
			doc_bow = tmp_dict.doc2bow(doc)
			scores_dict[q_id].append((d_id, cossim(new_query_bow, doc_bow)))
		sorted_scores = sorted(scores_dict[q_id], key=lambda item: item[1], reverse=True)
		scores_dict[q_id] = sorted_scores
	return scores_dict
