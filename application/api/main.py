from flask import Flask
from Crypto.PublicKey import RSA

from session import get_session_key


##########
# Routes #
##########

app = Flask(__name__)

@app.route("/")
def home():
    return "API Entry Point"

@app.route("/file")
def get_file():
    return ""


##################################
# Start TCP session key exchange #
##################################

get_session_key()
