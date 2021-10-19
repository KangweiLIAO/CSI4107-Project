# CSI4107-Assignment1
## Team Introduction
Langqing Zou 300035036<br>
&emsp;&emsp;Responsible for **Processing section**.<br>
&emsp;&emsp;Responsible for **Returing result file section**.<br>
&emsp;&emsp;Responsible for writing README.<br>
kangwei Liao 8568800<br> 
&emsp;&emsp;Responsible for **Indexing section**.<br>
&emsp;&emsp;Responsible for **Evaluation section**.<br>
&emsp;&emsp;Responsible for the code integration and final check.<br>
Aozhuo Zhang 300057882<br>
&emsp;&emsp;Responsible for **Retrieval and Ranking section**.<br>
&emsp;&emsp;Responsible for writing README.<br>
## System Introduction
### Functionality Description
Firstly, the program deals with the collection which is the tweet messages by tokenizing and removing stop words. As for the tokenization,
the program removes all the symbol in the collection. For example, "Latest::" will be "Latest". Also, the program scan the collection and remove
words appeared in stopwords.txt.<br>
Secondly, the program generated an inverted index based on the collection which has already disposed. The inverted index stores the terms and its 
document frequency and term frency.<br>
Thirdly, the program could retreve qureies and output the top 10 related Twitter comments.We use the cosine similarity formula for simiar calculate. 
### How to run it
First, you could download the whole file.
Second, Make sure you have the JDK version 16. Recomand ide is IDEA.
Third, you may compile all files and run main(Main.java)
### Algorithms and Data Structures Description
In index.java(For inverted index), we use hash map for data structures. We have three hash map, which is termMap,freqMap and docMap. TermMap are using to storge the terms, which is the doc which contain the spicific word, the freqMap storge the frequency of word, and the docMap storge the doc size.
The Similarity algotithm we use is the cosine similarity formula. In this algorithm, We need to first decompose the two pieces of text waiting to be compared into a list in terms of words. Then calculate the frequency of occurrence of the words in the query and in the text waiting to be compared, and generate the list. Finally, we use the list of two word frequencies to perform cosine similarity calculation, and calculate a similarity value, the larger it is, the more similar the two texts are.
