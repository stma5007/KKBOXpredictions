from nltk import tokenize
from collections import Counter
from nltk import ngrams, FreqDist
from collections import Counter
import pprint
from nltk.corpus import stopwords
import nltk


word_tokenizer = tokenize.TreebankWordTokenizer()
counter = Counter()



orig_stdout = sys.stdout
word_tokenizer = tokenize.TreebankWordTokenizer()
counter = Counter()
stopWords = set(stopwords.words('english'))

filename = 'all_speeches.txt'
def text_opener(rawtext):
    content = open(rawtext).read()
    sentence_list = tokenize.sent_tokenize(content)
    separate_words = word_tokenizer.tokenize_sents(sentence_list)
    words = [word for sentence in separate_words for word in sentence]
    words = [word for sentence in separate_words for word in sentence if word not in stopWords]

    return words

def grammies(file, n, how_many=10):
    trigrams = ngrams(data, n)
    dist = FreqDist(trigrams)

    return dist.most_common(how_many)

data = text_opener(filename)
tries = grammies(data,3)
print(tries)


