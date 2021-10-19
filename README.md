# CSI4107-Assignment1
## Team Introduction
Langqing Zou 300035036<br>
&emsp;&emsp;Responsible for **Processing section**.<br>
&emsp;&emsp;Responsible for **Returing result file section**.<br>
&emsp;&emsp;Responsible for writing README.<br>
kangwei Liao 8568800<br> 
&emsp;&emsp;Responsible for **Indexing Section**.<br>
&emsp;&emsp;Responsible for **Evaluation Section**.<br>
&emsp;&emsp;Responsible for the code integration and final check.<br>
Aozhuo Zhang 300057882<br>
&emsp;&emsp;Responsible for **Retrieval and Ranking Section**.<br>
&emsp;&emsp;Responsible for writing README.<br>
## System Introduction
### Functionality Description
Firstly, the program deals with the collection which is the tweet messages by tokenizing and removing stop words. As for the tokenization,
the program removes all the symbol in the collection. For example, "Latest::" will be "Latest". Also, the program scan the collection and remove
words appeared in stopwords.txt.<br>
Secondly, the program generated an inverted index based on the collection which is from above. The inverted index stores the terms and its 
document frequency and term frency.<br>
Thirdly, the program could retreve qureies and output the top 10 related Twitter comments by using the cosine similarity formula for simiar calculate. 
### How to run it
First, download the whole file named CSI4107-Assignment.
Second, make sure you have the JDK version 15+. Recomanded ide is IDEA.
Third, compile all files and run main(Main.java)
Last, you will get a result.txt of 49 test queries.
### Algorithms and Data Structures Description
**First Step**<br>
In the first step, we aim to dispose the collection, the Trec_microblog11.txt, by removing any stop-words, and tokenizing it as well. Firstly, we scan every term 
in the collection and remove the term which appears in the StopWords.txt.
As for the tokenization part, we try to delete all the symbols such as "/", ":", as well as any languages which are not English. Also, we take no account of wed address that showed in the every end of line. After all that efforts, we removing the valuable data from collection and replacing it with tokens that stands in for another, more valuable piece of information. <br>
Stop-words and collection after processed are all stored in Array Lists. We choose Arrary list since it has feasible size and elements can be inserted at or deleted from a particular position.<br>

**Second Step**<br>
We create a class named Index, representing the inverted indexing. We try to  optimize the value of collection by only storing unique terms. We use HashMap<String, LinkedList<Map.Entry<String, Double>>> to represent the term map, which is like {term:[(Document ID, Frequency)]}. Also, we use Map structure to stores frequency and document sizes. The reason we choose Map is that HashMap’s best and average case for Search, Insert and Delete is O(1) and worst case is O(n), which helps to save time.
<br>

**Thrid Step**<br>
we use the similarity algorithm. The Similarity algorithm we use is the cosine similarity formula. In this algorithm, We need to first decompose the two pieces of text waiting to be compared into a list in terms of words. Then calculate the frequency of occurrence of the words in the query and in the text waiting to be compared, and generate the list. Finally, we use the list of two word frequencies to perform cosine similarity calculation, and calculate a similarity value, the larger it is, the more similar the two texts are. Finaly we return the score of top 10 information.<br>

### Discusstion
There are 70487 vocabularies in inverted index. 

#### First 10 answers to queries 1:
1 Q0 30260724248870912 1 0.9923496054330064 Round1 <br>
1 Q0 30198105513140224 2 0.9632210242903613 Round1<br>
1 Q0 32504175552102401 3 0.889118635625648 Round1<br>
1 Q0 32158658863304705 4 0.889118635625648 Round1<br>
1 Q0 34952194402811904 5 0.889118635625648 Round1<br>
1 Q0 30236884051435520 6 0.889118635625648 Round1<br>
1 Q0 30251634873335810 7 0.8891186356256479 Round1<br>
1 Q0 30299217419304960 8 0.8891186356256479 Round1<br>
1 Q0 32415024995631105 9 0.8891186356256477 Round1<br>
1 Q0 30303184207478784 10 0.8891186356256477 Round1<br>
#### First 10 answers to queries 25:
25 Q0 31550836899323904 1 0.9914768881852257 Round25<br>
25 Q0 31738694356434944 2 0.9914768881852257 Round25<br>
25 Q0 32609015158542336 3 0.9914768881852256 Round25<br>
25 Q0 31286354960715777 4 0.9914768881852255 Round25<br>
25 Q0 30704222135652352 5 0.8152163455086991 Round25<br>
25 Q0 29993056316948480 6 0.815216345508699 Round25<br>
25 Q0 33609772196560896 7 0.815216345508699 Round25<br>
25 Q0 32955753920733184 8 0.815216345508699 Round25<br>
25 Q0 30767638397321217 9 0.815216345508699 Round25<br>
25 Q0 33633450548264960 10 0.815216345508699 Round25<br>

