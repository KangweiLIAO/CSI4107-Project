import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from gensim.models import Word2Vec

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words: list[str] = nltk.corpus.stopwords.words('english')
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


class CTColors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def add_stopwords(stopwords_path: str):
	try:
		# read stop words and put in a set
		custom_stopwords = open(stopwords_path, encoding='utf-8').readlines()
		stop_words.extend(custom_stopwords)  # add custom stopwords
	except FileNotFoundError as e:
		print(
			f"{CTColors.FAIL}Fail to add custom stop words, since specified stopwords file not found:{CTColors.ENDC}"
		)
		print(e)


def preprocess_str(raw_str: str):
	raw_str = raw_str.replace("\n", '').strip()  # format string
	word_tokens = word_tokenize(raw_str)  # tokenization
	lemmatized_str = [lemmatizer.lemmatize(w) for w in word_tokens if not w.lower() in stop_words]  # lemmatization
	return [stemmer.stem(w) for w in lemmatized_str]  # porter stemming and return


def read_queries(file_path: str) -> list[(str, list[str])]:
	q_id = ''
	q_list = []
	try:
		q_file = open(file_path, encoding='utf-8')
		for line in q_file:
			if "<num>" in line:
				q_id = str(int(re.sub("[^0-9]", "", line)))  # extract query id from the line
			elif "<title>" in line:
				# extract raw query string and preprocess it
				q_list.append((q_id, preprocess_str(line.replace("<title>", '').replace("</title>", ''))))
	except FileNotFoundError:
		print(f"{CTColors.FAIL}Specified query file not found.{CTColors.ENDC}")
	return q_list


def save_results(file_name: str, q_id: str, scores_list: (str, float)):
	file = open(file_name, 'a')
	rank = 1
	for doc_id, score in scores_list:
		file.write(f"{q_id} Q0 {doc_id} {rank} {score} Round1\n")
		rank += 1
	file.close()
