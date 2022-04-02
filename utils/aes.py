import os
import struct
import secrets

from Crypto.Cipher import AES, PKCS1_OAEP
import Crypto.Hash.MD5 as MD5
from Crypto.PublicKey import RSA


encoding = "UTF-8"
KEY_SIZE = 32
IV_SIZE = 16


def gen_rand_bytes(num_bytes=32):
    """ Return a random, cryptographically strong string of length num_bytes
    """
    return secrets.token_hex(num_bytes // 2)


def encrypt_string(data, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.encrypt(data.encode(encoding)).hex()


def decrypt_string(data, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(bytes.fromhex(data)).decode(encoding)


def encrypt_file(key, infile_path, outfile_path=None, chunksize=64*1024):
    """ Encrypts the given infile with AES in CBC mode and writes to outfile_path
    """
    if not outfile_path:
        outfile_path = infile_path + ".enc"

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    file_size = os.path.getsize(infile_path)

    with open(infile_path, "rb") as infile:
        with open(outfile_path, "wb") as outfile:
            outfile.write(struct.pack("<Q", file_size))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += (" " * (16 - len(chunk) % 16)).encode("utf-8")

                outfile.write(encryptor.encrypt(chunk))

    return outfile_path


def decrypt_file(key, infile_path, outfile_path, chunksize=24*1024):
    """ Decrypts the given file with AES with the given key.
    """
    if not outfile_path:
        outfile_path = os.path.splitext(infile_path)[0]

    with open(infile_path, "rb") as infile:
        size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(outfile_path, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(size)

    return outfile_path
    

def import_key(b):
    return RSA.importKey(b)


def create_hash(ptext):
    return MD5.new(ptext).digest()


def RSA_encrypt(key, msg):
    """ Encrypts a string message with given RSA key (public or private)
    """
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(msg)


def RSA_decrypt(key, msg):
    """ Decrypts a string message with given RSA key (public or private)
    """
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(msg)
