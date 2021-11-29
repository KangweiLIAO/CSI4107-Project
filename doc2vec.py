import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import retrieval_utils as utils

# Assume we have a dictionary that contains all words without symbols and stop-words
# tokenDic = [[words in doc1],[words in doc2],[words in doc3]....]
# dic = {doc1:[],doc2:[].....} {String:String}


RES_PATH = os.getcwd() + "/res/"
DOC_FILENAME = "Trec_microblog11.txt"

# extract every message as whole



"""
Returns the top 10 relevant documents.

:param dic: The dictionary of all documents:  dict{doc_id, list[word]}
:param query: The given query list: [string1, string2,....]
:return: The top 10 relevant documents.
"""


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


'''
:param queries: The raw queries, [(qid1, raw_query_content1),(qid2, raw_query_content2)...]
'''


# similarity scores dictionary dict{queryID, list[(doc_id, score)]}

def similarity_scores(dic, queries):
    # Load Model
    model = train_d2v_model(dic)
    # Predict
    results = {}
    for pair in queries:
        preprocess_query = utils.preprocess_str(pair[1])[0]
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


"""
Returns a dictionary contains docID and score.

:param sims: The top 10 documents.
:param query: The given query list: ["skye","is","kitty",.....]
:return: A dictionary contains docID and score
"""
