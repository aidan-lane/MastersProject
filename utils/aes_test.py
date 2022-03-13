"""Unittest for aes.py
"""

import unittest
import random
import string
from os.path import exists

from utils import aes

class TestAes(unittest.TestCase):

    def test_key_gen(self):
        """ Test AES private key generation
        """
        # Test default (32 bytes)
        key = aes.generate_key()
        self.assertTrue(len(key), 32)

        # Test user-specified amount
        new_len = 64
        key = aes.generate_key(new_len)
        self.assertTrue(len(key), new_len)


    def test_string(self):
        for _ in range(10):
            s = "".join(random.choices(string.ascii_lowercase, k=10))

            encoded = aes.encrypt_string(s)
            decoded = aes.decrypt_string(encoded)

            self.assertEqual(decoded, s)


    def test_encrypt_file(self):
        filename = "sample.txt"
        file = open(filename, "w")
        file.write("test")
        file.close()

        out_path = aes.encrypt_file(aes.generate_key(), filename)
        self.assertTrue(exists(out_path))
        self.assertRegex(out_path, ".*\.enc$")


    def test_aes(self):
        """Test encryption and decryption of a file using AES
        """
        filename = "sample.txt"
        dec_filename = "decrypted.txt"
        msg = "test_aes1234"

        key = aes.generate_key()

        file = open(filename, "w")
        file.write(msg)
        file.close()
        out_path = aes.encrypt_file(key, filename)

        aes.decrypt_file(key, out_path, dec_filename)
        dfile = open(dec_filename, "r")
        dec_msg = dfile.readline()
        dfile.close()

        self.assertEqual(dec_msg, msg)


if __name__ == "__main__":
    unittest.main()