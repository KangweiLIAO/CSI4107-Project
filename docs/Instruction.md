# Assignment 2 - Due Sunday Nov 28, at 10:00 PM

### Neural information retrieval system [50 points]

**Note: The assignment should be done in the formed groups of students.** 

You will implement an improved version of the Information Retrieval (IR) system you implemented in Assignment 1. This is a mini-competition to see which group will obtain the highest evaluation scores.

You will use the same collection of documents, the same test questions and the same evaluation measures. Note: Feel free to add or replace any components that could improve the evaluation scores, and to use any tools or software as long as you give credit properly.

**The goals of this assignment is to explore recent neural information retrieval methods** (based on deep learning, transformers, BERT-like models) in order to achieve better evaluation scores than in Assignment 1. You can get more ideas from the article: https://arxiv.org/pdf/2010.06467.pdf

Perform **at least two experiments** from the list below or other ideas of advanced methods:

1. Use your system for Assignment 1 to produce initial results (1000 documents for each query), then re-rank them based on a new similarity scores between the query and each selected document. You can produce vectors for the query and each of the selected documents using various versions of sent2vec, doc2vec, BERT, or the universal sentence encoder. You can also use pre-trained word embeddings and assemble them to produce query/document embeddings.

4. Query vector modification or query expansion based on pretrained word embeddings or other methods. For example, add synonyms to the query if there is similarity with more than one word in the query (or with the whole query vector). You can use pre-trained word embeddings (such as FastText, word2vec, GloVe, and others), preferably some build on a Twitter corpus, to be closer to your collection of documents.
Use BERT or other neural models from the beginning, without the need on an initial classical IR system, to compute the similarity between the query and every document in the collection. This probably will take too long time, but look for ways to reduce the number of operations needed, especially if your system for Assignment 1 is not functional. For example, you can use a simple boolean index to restrict the calculations only to documents that have at least one query word.
Try at least two different advanced neural retrieval methods. Discuss in your report if they were able to achieve better results than you system for Assignment 1. [10 points each]

5. Produce a file called Results with the results for all the 49 test queries, in the required format, for your best system. [10 points]

Evaluation: report the MAP and P@10 score for the methods you tried and highlight the best scores and for what method they were. [5 points]

### Submission instructions:

   - write a README file (pdf, plain text, or Word format) **[15 points for this report]** including:

     - your names and student numbers. **Specify how the tasks were divided between the team members (if this info is not provided, the penalty is 10 points)**.
     - a detailed note about the functionality of your programs
     - complete instructions on how to run them
     - Explain the algorithms, data structures, and optimizations that you used. Include the first 10 answers to queries 3 and 20. Discuss your results for all the methods you used.
   
   - include the file named Results with the results for all the 49 test queries, in the required format, for you best system.
   - make sure all your programs run correctly.
   - submit your assignment, including programs, README file, and Results file, as a zip file through BrightSpace.
   - don't include the initial text collection or any external tools. 