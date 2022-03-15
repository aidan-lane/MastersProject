
def extract_ngrams(word, n):
    if len(word) - n < 0:
        return word

    ngrams = set()
    for i in range(len(word) - n + 1):
        ngrams.add(word[i:min(i + n, len(word))])
    return ngrams