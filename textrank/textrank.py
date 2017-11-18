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

def similarity(s1, s2):
    if not len(s1) or not len(s2):
        return 0.0
    return len(s1.intersection(s2))/(1.0 * (len(s1) + len(s2)))

def textrank(text):
    sentences = sent_tokenize(text)
    for i, s in enumerate(sentences):
        lines = s.splitlines()
        [lines.pop(j) if len(l) < 1 else lines for j, l in enumerate(lines)]
        sentences.pop(i)
        sentences.extend(lines)

    tokenizer = RegexpTokenizer(r'\w+')
    # lmtzr = RussianStemmer()
    lmtzr = EnglishStemmer()
    words = [set(lmtzr.stem(word) for word in tokenizer.tokenize(
        sentence.lower()))
             for sentence in sentences]

    pairs = combinations(range(len(sentences)), 2)
    scores = [(i, j, similarity(words[i], words[j])) for i, j in pairs]
    scores = filter(lambda x: x[2], scores)

    g = nx.Graph()
    g.add_weighted_edges_from(scores)
    pr = nx.pagerank(g)

    return sorted(((i, pr[i], s) for i, s in enumerate(sentences) if i in pr),
                  key=lambda x: pr[x[0]], reverse=True)

def extract(text, n=5):
    tr = textrank(text)
    top_n = sorted(tr[:n])
    return ' '.join(x[2] for x in top_n)


# f = open("./bbc/tennis/001.txt", 'r')
# text = f.read()
# f.close()
#
# result = extract(text)
# print(result)