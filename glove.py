import gensim.downloader as api
from inverted_index import InvertedIndex

api.load("glove-twitter-200")


def similarity_scores(inv_index: InvertedIndex, queries):
	pass
