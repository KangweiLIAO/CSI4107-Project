import time
import retrieval_utils as utils
from retrieval_utils import CTColors
from inverted_index import InvertedIndex
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def similarity_scores(inv_index: InvertedIndex, queries: list[(str, list[str])]):
	pass
