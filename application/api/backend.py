from flask import Flask
from flask_cors import CORS

from Crypto.PublicKey import RSA

from session import get_session_key


##########
# Routes #
##########

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API Entry Point"


@app.route("/matches", methods=["GET"])
def matches():
    return "test"


@app.route("/file")
def get_file():
    return ""


##################################
# Start TCP session key exchange #
##################################

session_key, iv = get_session_key()

app.run()
