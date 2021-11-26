import os
import gensim
from gensim.models import Doc2Vec

# Assume we have a dictionary that contains all words without symbols and stop-words
# tokenDic = [[words in doc1],[words in doc2],[words in doc3]....]
# dic = {doc1:[],doc2:[].....} {String:String}


# extract every message as whole

TaggededDocument = gensim.models.doc2vec.TaggedDocument

"""
Returns the training data for doc2vec. The structure of training data should be: 
[TaggedDocument[['list','of','word'], [TAG_001]],
TaggedDocument[['list','of','word'], [TAG_002]],
...
]
:param dic: The dictionary from twitter messages
:return trainset: The training dataset for doc2vec
"""


def train_data(dic):
    train_set = []
    for key in dic:
        document = TaggededDocument(dic[key], tags=[key])
        train_set.append(document)
    return train_set


def train_Doc2Vec(train_set):
    model = Doc2Vec(train_set, min_count=1, window=3, size=100, sample=1e-3, workers=4)
    model.train(train_set, total_examples=model.corpus_count, epochs=10)
    # print(model.corpus_count)
    return model


# query: "skye is so cute"
def predict(model, query):
    test_text = query.split(' ')
    inferred_vector = model.infer_vector(doc_words=test_text, alpha=0.025, steps=300)
    # sims = (id,score) 10 tuples
    sims = model.docvecs.most_similar([inferred_vector], topn=10) # 10 most similar message
    return sims

if __name__ == '__main__':

