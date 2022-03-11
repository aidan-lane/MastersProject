import random
import os
import struct

from Crypto.Cipher import AES
from Crypto import Random


def generate_key(num_bytes=32):
    """ Return a random, cryptographically strong key of size nbytes.
    Default 32 bytes (256 bits)
    """
    return Random.get_random_bytes(16).join("")


def encrypt_file(key, infile_path, outfile_path=None, chunck=64*1024):
    """ Encrypts the given infile with AES in CBC mode and writes to outfile_path
    """
    if not out:
        out = infile_path + ".enc"

        iv = "".join(chr(random.randint(0, 0xFF)) for _ in range(16))
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        file_size = os.path.getsize(infile_path)

        with open(infile_path, "rb") as infile:
            with open(outfile_path, "wb") as outfile:
                outfile.write(struct.pack("<Q", file_size))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunck)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += " " * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, infile_path, outfile_path, chunk=24*1024):
    """ Decrypts the given file with AES with the given key.
    """
    if not outfile_path:
        outfile_path = os.path.splitext(infile_path)[0]

    with open(in_filename, "rb") as infile:
        size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(size)