# CSI4107 Assignment 2
## Teamwork Distribution
Langqing Zou (300035036)
### Responsible for **Doc2Vec Algorithm**
I use doc2vec


Kangwei Liao (8568800)
### Responsible for **Wor2Vec Algorithm**
### Responsible for **Code Integration** and **Final Check**


Aozhuo Zhang (300057882)
- Responsible for ** **.

## Steps To Run (Python 3.9 required)
1. Make sure the python version >= 3.9
2. Install the python library [virtualenv] using command ```python3 -m pip install --user virtualenv```
3. Create a virtual environment in project directory using ```python3 -m venv env```
4. Activate the virtual environment using ```source env/bin/activate``` (Mac OS)
5. Install the packages specified in ```requirements.txt```
6. Run ```main.py``` using the **Python interpreter in virtual environment**

## The functionality of the programs
Firstly, the program deals with the collection which is the tweet messages by tokenizing and removing stop words. As for the tokenization,
the program removes all the symbol in the collection. For example, "Latest::" will be "Latest". Also, the program scan the collection and remove
words appeared in stopwords.txt.<br>
Secondly, the program generated an inverted index based on the collection which is from above. The inverted index stores the terms and its 
document frequency and term frency.<br>
Thirdly, the program could retreve qureies and output the top 10 related Twitter comments by using the tf-idf algorithm, word2vec algorithm and doc2vec algorithm respectively for simiar calculate.


## Algorithms and Data Structures
We use three algotithms here. 
### TF-IDF
### Word2Vec
### Doc2Vec

## First 10 answers to queries 3 and 20

### TF-IDF Algorithm
#### Screenshot
#### MAP and P@10
### Word2Vec Algorithm
#### Screenshot
#### MAP and P@10
### Doc2Vec Algorithm
#### Screenshot
#### MAP and P@10
