import os
import glob
import sys
from pathlib import Path

import string
import numpy as np
from collections import Counter
import math

def removePunct(s):
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in s if ch not in exclude)
    return s


def getStopWords(fin):
    return set([term.strip() for term in fin])


def removeStopWords(d, stopwords):
    for term in set(d.keys()):
        if term in stopwords:
            del d[term]


# ========== FREQUENCIES ==========
# removePunct(x.lower()).encode('utf-8')

def getTermFrequencies(fin):
    tf = Counter()
    for line in fin: tf.update(
        map(lambda x: removePunct(x.lower()), line.split()))
    return tf


def getDocumentFrequencies(tf):
    df = Counter()
    for d in tf: df.update(d.keys())
    return df


def getDocumentFrequency(df, term):
    if term in df:
        return df[term] + 1
    else:
        return 1


# ========== TF-IDF ==========

def getTFIDF(tf, df, dc):
    return tf * math.log(float(dc) / df)


def getTFIDFs(term_frequencies, doc_frequencies, doc_count):
    tf_idf = {}
    for doc in term_frequencies:
        for (term, frequency) in doc.items():
            tf_idf[term] = getTFIDF(frequency,
                                    getDocumentFrequency(doc_frequencies, term),
                                    doc_count)
    return tf_idf
    # return [{word: getTFIDF(frequency, getDocumentFrequency(df, word), dc) for (word, frequency) in
    #          doc.items()} for doc in tf]


def get_TFIDF_scores(DIR, EXT):
    # trnFiles = sorted(glob.glob(os.path.join(DIR, '*.' + EXT)))
    trnFiles = sorted(Path(DIR).glob('**/*.' + EXT))
    trnTF = [getTermFrequencies(open(str(filename))) for filename in trnFiles]
    trnDF = getDocumentFrequencies(trnTF)
    trnDC = len(trnFiles)
    trnTFIDF = getTFIDFs(trnTF, trnDF, trnDC)
    return trnTFIDF
