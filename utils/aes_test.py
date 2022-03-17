"""Unittest for aes.py
"""

import unittest
import random
import string
from os.path import exists
import string

from utils import aes

class TestAes(unittest.TestCase):

    def test_key_gen(self):
        """ Test AES private key generation
        """
        # Test default (32 bytes)
        key = aes.gen_rand_bytes(aes.KEY_SIZE)
        self.assertTrue(len(key), aes.KEY_SIZE)

        # Test user-specified amount
        new_len = 64
        key = aes.gen_rand_bytes(new_len)
        self.assertTrue(len(key), new_len)


    def test_string(self):
        key = aes.gen_rand_bytes(aes.KEY_SIZE)
        iv = aes.gen_rand_bytes(aes.IV_SIZE)

        for _ in range(10):
            s = "".join(random.choices(string.ascii_lowercase, k=10))

            encrypted = aes.encrypt_string(s, key, iv)
            decrypted = aes.decrypt_string(encrypted, key, iv)

            # Ensure encrypted is a hex string
            self.assertTrue(all(c in string.hexdigits for c in encrypted))
            self.assertEqual(decrypted, s)


    def test_encrypt_file(self):
        filename = "sample.txt"
        file = open(filename, "w")
        file.write("test")
        file.close()

        out_path = aes.encrypt_file(aes.gen_rand_bytes(aes.KEY_SIZE), filename)
        self.assertTrue(exists(out_path))
        self.assertRegex(out_path, ".*\.enc$")


    def test_aes(self):
        """Test encryption and decryption of a file using AES
        """
        filename = "sample.txt"
        dec_filename = "decrypted.txt"
        msg = "test_aes1234"

        key = aes.gen_rand_bytes(aes.KEY_SIZE)

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