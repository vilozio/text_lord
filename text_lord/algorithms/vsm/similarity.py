import math


def cosine(d1, d2):
    numerator = 0
    denominator1 = 0
    denominator2 = 0

    for (k, v) in d1.items():
        denominator1 += v ** 2
        if k in d2:
            numerator += v * d2[k]

    for (k, v) in d2.items():
        denominator2 += v ** 2

    return 1 - (numerator / (math.sqrt(denominator1) * math.sqrt(denominator2)))