from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
from itertools import combinations
import networkx as nx

f = open("./bbc/tennis/001.txt", 'r')
text = f.read()
f.close()

def similarity(s1, s2):
    if not len(s1) or not len(s2):
        return 0.0
    return len(s1.intersection(s2))/(1.0 * (len(s1) + len(s2)))

sentences = sent_tokenize(text)

tokenizer = RegexpTokenizer(r'\w+')
lmtzr = EnglishStemmer()
words = [set(lmtzr.stem(word) for word in tokenizer.tokenize(sentence.lower()))
         for sentence in sentences]
print(words)

pairs = combinations(range(len(sentences)), 2)
scores = [(i, j, similarity(words[i], words[j])) for i, j in pairs]
scores = filter(lambda x: x[2], scores)

g = nx.Graph()
g.add_weighted_edges_from(scores)
pr = nx.pagerank(g)

result = sorted(((i, pr[i], s) for i, s in enumerate(sentences) if i in pr),
                key=lambda x: pr[x[0]], reverse=True)

print(result)
