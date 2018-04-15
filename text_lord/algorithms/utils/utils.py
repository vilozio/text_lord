import string
import os
import sys
from nltk import tokenize
import codecs


# reload(sys)
# sys.setdefaultencoding("utf-8")


def removePunct(s):
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in s if ch not in exclude)
    return s


# def getSentences(doc_dir, doc_id):
#     i = 0
#     for subdir, dirs, files in os.walk(doc_dir):
#         files.sort()
#         for file in files:
#             filepath = subdir + file
#             if i == doc_id:
#                 with open(filepath) as doc:
#                     sentences = tokenize.sent_tokenize(doc.read())
#                     return sentences
#
#             else:
#                 i = i + 1

def getSentences(paths, doc_id):
    filepath = paths[doc_id]
    with open(filepath) as doc:
        sentences = tokenize.sent_tokenize(doc.read())
        return sentences


def get_sentences(text):
    return tokenize.sent_tokenize(text)


def mapTFIDFScores(sentence, scores):
    words = sentence.split()
    mapping = dict((w, scores[removePunct(w.lower())]) for w in words)
    return mapping


def map_TFIDF_scores(sentence, scores):
    mapping = {}
    words = sentence.split()
    for word in words:
        formated = removePunct(word.lower())
        score = scores[formated]
        mapping[formated] = score
    return mapping
