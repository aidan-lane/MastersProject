
def extract_ngrams(word, n):
    if len(word) - n < 0:
        return word

    ngrams = []
    for i in range(len(word) - n + 1):
        ngrams.append(word[i:min(i + n, len(word))])
    return ngrams