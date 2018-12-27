#!/usr/bin/python
import re
import sys
from collections import Counter
import nltk
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk import word_tokenize, sent_tokenize
stemmer = SnowballStemmer('english')
COUNTS_FILE_NAME = "output_full_stemmed_stopwords.txt"
CLASSES_LIST_FILE_NAME = "classes.txt"
STOPWORDS_FILE_NAME = "stopwords.txt"
ALPHA = 0.1
VOCABULARY_SIZE = 300000

def remove_till_first_quote(text):
    regex = r"^(.*?)\""
    text = re.sub(regex, '', text)
    return text

def remove_unicode(text):
    """Replace unicode codes like \uxxxx with space"""
    regex = r"(\\u....)"
    text = re.sub(regex, ' ', text)
    return text

def denoise_text(text):
    text = remove_till_first_quote(text)
    text = remove_unicode(text)
    text = remove_punctuation(text)
    return text

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(text):
    """Remove punctuation and replace with space"""
    text = re.sub(r'[^\w\s]', ' ', text)
    return text


with open(filepath) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       print("Line {}: {}".format(cnt, line.strip()))
       line = fp.readline()
       cnt += 1
with open(filepath) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       print("Line {}: {}".format(cnt, line.strip()))
       line = fp.readline()
       cnt += 1


f = open(COUNTS_FILE_NAME, "r")
table = {}
wordsInClass = {}
for line in f.readlines():
    line = line.strip()
    splitLine = line.split()
    wordAndClass = splitLine[0].split(',')
    count = int(splitLine[1])
    word = wordAndClass[0]
    documentClass = wordAndClass[1]
    table[(word, documentClass)] = count
    if documentClass in wordsInClass:
        wordsInClass[documentClass] += count
    else:
        wordsInClass[documentClass] = count
f.close()

f = open(CLASSES_LIST_FILE_NAME, "r")
documentClasses = []
for line in f.readlines():
    line = line.strip()
    documentClasses.append(line)
f.close()

stopwords = []
f = open(STOPWORDS_FILE_NAME, "r")
for line in f.readlines():
    line = line.strip()
    if(line):
        stopwords.append(line)
f.close()




for line in sys.stdin:
    line = line.strip()
    splitLine = line.split('\t', 2)
    document = splitLine[1]
    classes = splitLine[0]
    classes = classes.strip()
    classes = classes.split(',')
    documentsGroundTruthClass = classes
    document = denoise_text(document)
    words = document.split()
    words = to_lowercase(words)
    new_words = []
    for word in words:
        if word in stopwords:
            continue
        new_words.append(stemmer.stem(word))
    words = list(set(new_words)) #only need 1 occurence

    bestP = 0.0
    pClass = 'Articles_containing_video_clips'
    for testClass in documentClasses:
        P = 1
        for word in words:
            if (word, testClass) in table:
                count = table[(word, testClass)]
            else:
                count = 0
            currP = float(count + ALPHA)/float(wordsInClass[testClass] + ALPHA*VOCABULARY_SIZE)
            P *= currP
            if (P < bestP):
                break
        if (P > bestP):
            bestP = P
            pClass = testClass
    numDone += 1
    if pClass in documentsGroundTruthClass:
        print "%s\t%s" % ("Correct", 1)
        numCorrect += 1
    else:
        print "%s\t%s" % ("Wrong", 1)
        numWrong += 1

    # for myword in words:
    #     for myclass in classes:
    #         print '%s,%s\t%s' % (myword, myclass, 1)
