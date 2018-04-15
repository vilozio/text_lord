import string
from collections import Counter
import math


def remove_punct(s):
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in s if ch not in exclude)
    return s


def get_stop_words(fin):
    return set([term.strip() for term in fin])


def remove_stop_words(d, stopwords):
    for term in set(d.keys()):
        if term in stopwords:
            del d[term]


def count_term_frequencies(text):
    tf = Counter()
    tf.update(map(lambda x: remove_punct(x.lower()), text.split()))
    return tf


def count_all_frequencies(term_frequencies):
    df = Counter()
    for path, tf in term_frequencies.items():
        df.update(tf.keys())
    return df


def get_document_frequency(all_frequencies, term):
    if term in all_frequencies:
        return all_frequencies[term] + 1
    else:
        return 1


# ========== TF-IDF ==========

def tfidf(tf, df, dc):
    return tf * math.log(float(dc) / df)


def tfidf_by_doc(term_frequencies, all_frequencies, doc_count):
    tf_idf = {}
    for doc_id, term_freq in term_frequencies.items():
        for term, frequency in term_freq.items():
            doc_frequency = get_document_frequency(all_frequencies, term)
            term_score = tfidf(frequency, doc_frequency, doc_count)
            if doc_id not in tf_idf:
                tf_idf[doc_id] = {}
            tf_idf[doc_id].update({term: term_score})
    return tf_idf


def get_TFIDF_scores(texts):
    term_frequencies_by_doc = {path: count_term_frequencies(text)
                               for path, text in texts.items()}
    all_frequencies = count_all_frequencies(term_frequencies_by_doc)
    doc_count = len(texts)
    tfidf_scores = tfidf_by_doc(term_frequencies_by_doc, all_frequencies,
                                doc_count)
    return tfidf_scores
