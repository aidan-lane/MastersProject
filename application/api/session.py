from msilib.schema import Signature
import pickle
import socket

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as pksig
from Crypto.Hash import SHA384

def get_session_key():
    host = "localhost"
    port = 9999

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Generate a new RSA key pair for this session and send our public key to server
    key = RSA.generate(2048)

    # Create signature by encrypting a hashed plaintext with the private key
    mhash = SHA384.new("textbook")
    mhash.update()
    signature = pksig.new(key).sign(mhash)

    sock.send(pickle.dumps( (key.publickey().exportKey(), signature) ))

    #session_key, iv = pickle.loads(sock.recv(4096))

    sock.close()
    return None