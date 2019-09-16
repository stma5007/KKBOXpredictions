from collections import Counter
from nltk import tokenize
from nltk import ngrams
import emoji
from nltk import FreqDist
import matplotlib.pyplot
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import pprint
import sys
import csv

orig_stdout = sys.stdout
word_tokenizer = tokenize.TreebankWordTokenizer()
counter = Counter()
exclude_stop = open("stopwordsDan.txt").read()
exclude_real_agent = open('rs_bs.txt').read()

def text_opener(rawtext):
    content = open(rawtext).read()
    sentence_list = tokenize.sent_tokenize(content)
    separate_words = word_tokenizer.tokenize_sents(sentence_list)
    words = [word for sentence in separate_words for word in sentence]
    words = [item for item in words if item not in exclude_stop and item not in exclude_real_agent]

    return words

data = text_opener('real_estaten.txt')

def TFdict(data):
    tfdict = {} # create dictionary
    for word in data:
        if word in tfdict:
            tfdict[word] += 1
        else:
            tfdict[word] = 1

    for word in tfdict:
        tfdict[word] = tfdict[word] / len(data)

    return tfdict

term_freq = TFdict(data)

def computeCountDict(data):
    countDict = {}

    for word in data:
        if word in countDict:
            countDict[word] += 1
        else:
            countDict[word] = 1
    return countDict

countDict = computeCountDict(data)

def idf():

    idf_dict = {}
    for word in countDict:
        idf_dict[word] = math.log10(len(data) / countDict[word])

    return idf_dict

def TFIDF(term_frequency_dict):

    TFIDFdict = {}

    for word in term_frequency_dict:
        TFIDFdict[word] = term_frequency_dict[word] * idf[word]

    return TFIDFdict
TFIDF = [TFdict(term_freq) for data in term_freq]

print(TFIDF)


# pprint.pprint(TFIDF) Uncommenct, but will take a long time to print
