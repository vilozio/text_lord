# процент эффективности по каждой статье
# средняя по рубрике - сделать график
# результат - получение красивой поданой информации с выводами
# показать разные сравнение (русский, английский)
# автоопределение языка
# практическое применение
from itertools import combinations
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk.stem.snowball import RussianStemmer, EnglishStemmer
import networkx as nx
from logging import getLogger

logger = getLogger(__name__)


def similarity(s1, s2):
    if not len(s1) or not len(s2):
        return 0.0
    return len(s1.intersection(s2))/(1.0 * (len(s1) + len(s2)))


def textrank(text):
    """Return the TextRank of the sentences in the text.
    
        Returns
        -------
        textrank : list
            List of sorted tuples by pagerank for sentences
            
            >>> [(number_of_sentence, pagerank, sentence), ...]
        
        G: graph
            A NetworkX graph of sentences with weighted edges
    """
    sentences = sent_tokenize(text)
    # separate new lines as new sentences
    for i, s in enumerate(sentences):
        lines = s.splitlines()
        [lines.pop(j) for j, l in enumerate(lines) if len(l) < 1]
        sentences.pop(i)
        sentences.extend(lines)

    tokenizer = RegexpTokenizer(r'\w+')
    # lmtzr = RussianStemmer()
    lmtzr = EnglishStemmer()
    # tokenize words and find unique stems for them
    stem_words_for_sentence = [set(lmtzr.stem(word)
                                   for word in
                                   tokenizer.tokenize(sentence.lower()))
                               for sentence in sentences]
    logger.debug('Stem words: {}'.format(stem_words_for_sentence))

    pair_sentences = combinations(range(len(sentences)), 2)
    scores = [(i, j, similarity(stem_words_for_sentence[i],
                                stem_words_for_sentence[j]))
              for i, j in pair_sentences]
    logger.debug('Scores for sentences: {}'.format(scores))
    # filter scores with existing similarity
    scores = filter(lambda x: x[2], scores)

    G = nx.Graph()
    # graph (u,v,w) - (sentence1 idx, sentence2 idx, similarity)
    G.add_weighted_edges_from(scores)
    pr = nx.pagerank(G)

    logger.debug('PageRank for sentences: {}'.format(pr))

    sorted_textrank = sorted(
        ((i, pr[i], s) for i, s in enumerate(sentences) if i in pr),
        key=lambda x: pr[x[0]],
        reverse=True)

    return sorted_textrank, G


def extract(text, n=5):
    tr, G = textrank(text)
    top_n = sorted(tr[:n])
    return ' '.join(x[2] for x in top_n)
