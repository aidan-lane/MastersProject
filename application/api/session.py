import pickle
import socket

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5 as pksig
from Crypto.Hash import SHA384


encoding = "UTF-8"


def get_session_key():
    host = "localhost"
    port = 9999

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Generate a new RSA key pair for this session and send our public key to server
    key = RSA.generate(2048)

    # Create signature by encrypting a hashed plaintext with the private key
    mhash = SHA384.new("textbook".encode(encoding))
    signature = pksig.new(key).sign(mhash)

    # Send public key and signature
    sock.send(pickle.dumps( (key.publickey().exportKey(), signature) ))

    # Get encrypted session key and IV from server and decrypt
    session_key, iv = pickle.loads(sock.recv(4096))
    session_key = PKCS1_OAEP.new(key).decrypt(session_key).decode(encoding)
    iv = PKCS1_OAEP.new(key).decrypt(iv).decode(encoding)

    sock.close()
    return session_key, iv