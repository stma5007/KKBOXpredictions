import spacy 
import nltk
import textstat
from textstat.textstat import textstatistics, easy_word_set, legacy_round 
from nltk import tokenize
from nltk import pos_tag_sents
from nltk import ngrams, FreqDist

filenames = #ENTER FILENAMES

word_tokenizer = tokenize.TreebankWordTokenizer()
nlp = spacy.load("en_core_web_sm")

#Need to find a better way to open all texts, rightn now os package is annoying

adjective_counter = 0
all_speeches = []
for filename in filenames:
    with open(filename) as f: 
        for speech in f.readlines():
            all_speeches.append(speech)
            speech = nlp(speech)            
                    
        for token in speech:
            if token.pos_ == 'ADJ':
                adjective_counter += 1

print(adjective_counter)

filename = 'all_speeches.txt'

def all_words(rawtext):
    content = open(rawtext).read()
    sentence_list = tokenize.sent_tokenize(content)
    separate_words = word_tokenizer.tokenize_sents(sentence_list)
    words = [word for sentence in separate_words for word in sentence]
    return words

def sentences(rawtext):
    all_sentences = []
    content = open(rawtext).read()
    all_text = nltk.sent_tokenize(content)
    for sentences in all_text:
        tokens_ = nltk.word_tokenize(sentences)
        all_sentences.append(tokens_)

    return all_sentences

def average_sent_length(rawtext):
    words = all_words(rawtext)
    sents = sentences(rawtext)

    avg = float(len(words) / len(sents))

    return avg

def syllables_counter(rawtext):
    words = all_words(rawtext)
    return syllables_count(words)

## Readability

readability = []
for filename in filenames:
    with open(filename) as f: 
        for speech in f.readlines():
            speeches = speech.strip("\n")
            readability.append(textstat.flesch_reading_ease(speeches))
            
average_readability = [sum(readability) / len(readability)]
print(average_readability)







""" 

    :Other metrics:  

print(textstat.flesch_reading_ease(all_words(filename)))
print(textstat.smog_index(filename))
print(textstat.flesch_kincaid_grade(filename))
print(textstat.coleman_liau_index(filename))
print(textstat.difficult_words(filename))
print(textstat.text_standard(filename))

    :Scores: 

* 90-100 : Very Easy 
* 80-89 : Easy 
* 70-79 : Fairly Easy 
* 60-69 : Standard 
* 50-59 : Fairly Difficult 
* 30-49 : Difficult 
* 0-29 : Very Confusing

""" 
