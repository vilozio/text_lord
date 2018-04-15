import numpy as np
import math

from ..vsm import tfidf
from ..utils import utils


class LexRank(object):
    def __init__(self, texts):
        self.texts = texts
        self.tfidf_scores = tfidf.get_TFIDF_scores(texts)
        self.matrix = []
        self.sentences = []

    def summarization(self, similarity_func, normalize_func):
        matrices = []
        sentences = []
        for path, text in self.texts.items():
            curr_sentences = utils.get_sentences(text)
            curr_num_of_sentences = len(curr_sentences)
            sentences.append(curr_sentences)
            matrices.append(self.build_similarity_matrix(curr_num_of_sentences,
                                                         curr_sentences, path,
                                                         similarity_func,
                                                         normalize_func))
        self.matrix = matrices
        self.sentences = sentences

    def build_similarity_matrix(self, num_of_sentences, sentences, doc_id,
                                similarity_func, normalize_func):
        matrix = np.zeros((num_of_sentences, num_of_sentences))
        for x in range(0, num_of_sentences):
            vec_x = utils.map_TFIDF_scores(sentences[x],
                                           self.tfidf_scores[doc_id])
            for y in range(0, num_of_sentences):
                if x == y:
                    matrix[x][y] = 1.0
                    continue
                vec_y = utils.map_TFIDF_scores(sentences[y],
                                               self.tfidf_scores[doc_id])
                score = similarity_func(vec_x, vec_y)
                if np.isnan(score):
                    score = 0.0
                matrix[x][y] = score

        # Normalize each row of scores
        for x in range(0, num_of_sentences):
            matrix[x] = normalize_func(matrix[x], num_of_sentences)
        return matrix

    def rank(self, similarity_threshold, epsilon, iterations, continuous,
             damp):
        return multi_doc_rank(self.matrix, self.sentences,
                              similarity_threshold, epsilon, iterations,
                              continuous, damp)


def multi_doc_rank(matrices, sentences, similarity_threshold, epsilon,
                   iterations, continuous, damp):
    rankings = []
    for x in range(0, len(matrices)):
        num_of_sentences = len(matrices[x][0])
        similarity_matrix = reflect_over_YX(matrices[x], num_of_sentences)
        transition_matrix = build_transition_matrix(similarity_matrix,
                                                    num_of_sentences,
                                                    similarity_threshold,
                                                    continuous)
        rank, score = power_iteration(transition_matrix, num_of_sentences,
                                      epsilon, iterations, damp)
        rankings.append(rank)
    return rankings, sentences


# Reflect Scores of the matrix over the line y = x b/c index order of
# sentence doesn't matter
def reflect_over_YX(matrix, num_of_sentences):
    result = np.zeros((num_of_sentences, num_of_sentences))
    for x in range(0, num_of_sentences):
        for y in range(0, x + 1):
            result[x][y] = result[y][x] = matrix[x][y]
    return result


# Build transition probability matrix with threshold | continuous
def build_transition_matrix(similarity_matrix, num_of_sentences,
                            similarity_threshold=.1, continuous=True):
    transition_matrix = np.zeros((num_of_sentences, num_of_sentences))
    for x in range(0, num_of_sentences):
        degree = 0
        for y in range(0, num_of_sentences):
            if similarity_matrix[x][y] > similarity_threshold:
                if continuous:
                    transition_matrix[x][y] = similarity_matrix[x][y]
                    degree += similarity_matrix[x][y]
                else:
                    transition_matrix[x][y] = 1
                    degree += 1
        for y in range(0, num_of_sentences):
            transition_matrix[x][y] /= degree

    return transition_matrix


def power_iteration(stochastic_matrix, num_of_sentences, epsilon, max_iterations,
                    damp):
    if damp > 0:
        curr_matrix = apply_damping_factor(stochastic_matrix, num_of_sentences,
                                           damp).transpose()
    else:
        curr_matrix = stochastic_matrix.transpose()
    curr_vec = np.zeros((num_of_sentences, 1))
    prev_vec = np.zeros((num_of_sentences, 1))
    curr_vec.fill(1.0 / num_of_sentences)

    for x in range(0, max_iterations):
        prev_vec = curr_vec
        curr_vec = np.dot(curr_matrix, curr_vec)
        error = 0.0
        for y in range(0, num_of_sentences):
            error += math.sqrt(abs(curr_vec[y][0] - prev_vec[y][0]))
        if error < math.sqrt(epsilon):
            break

    # Scores sorted from lowest to biggest
    scores = [curr_vec[x][0] for x in range(0, num_of_sentences)]

    # Ranking based on biggest score to lowest so indexes are reversed
    rankings = np.argsort(scores)
    rankings = rankings[::-1]
    return rankings, scores


def apply_damping_factor(matrix, N, d):
    # 1-dB
    matrix = np.multiply(matrix, 1 - d)
    dU = np.zeros((N, N))
    dU.fill(1.0 / N)
    return dU + matrix
