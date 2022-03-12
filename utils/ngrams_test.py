"""Unittest for ngrams.py
"""

import unittest
from os.path import exists

from utils import ngrams

class TestNgrams(unittest.TestCase):

    def test_ngram_smaller(self):
        """Test when ngram size is larger than given word
        """
        word = "abc"
        grams = ngrams.extract_ngrams(word, 4)
        self.assertTrue(len(grams), 1)
        self.assertTrue(len(grams[0]), 3)


    def test_ngram_larger(self):
        """ Test when word is divided into multiple ngrams
        """
        word = "testword"
        answer = ["test", "estw", "stwo", "twor", "word"]
        grams = ngrams.extract_ngrams(word, 4)

        self.assertTrue(len(grams), len(answer))
        self.assertSequenceEqual(grams, answer)


if __name__ == "__main__":
    unittest.main()