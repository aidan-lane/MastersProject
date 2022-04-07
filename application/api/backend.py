import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2 import service_account
import psycopg2 as sql
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from google.cloud import storage
from Crypto.PublicKey import RSA

from session import get_session_key
from utils import aes, ngrams

##############################
# Google Cloud Clients Setup #
##############################

# Credentials
key_path = "server/service_account.json"
credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Cloud Storage
storage_client = storage.Client(credentials=credentials, 
    project=credentials.project_id,)
file_bucket_name = "al-enc-files"

# Connect to CloudSQL instance
load_dotenv(os.getcwd() + "/server/.env")  # Get relative .env file from server
conn = sql.connect(database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASS"), host=os.getenv("DB_HOST"))
cursor = conn.cursor()


##################################
# Start TCP session key exchange #
##################################

session_key, iv = get_session_key()


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
    # Get request params
    keyword = request.args.get("keyword")
    nsize = int(request.args.get("nsize"))

    # Generate n-grams for this keyword
    n_arr = [aes.encrypt_string(ngram, session_key, iv) for 
        ngram in ngrams.extract_ngrams(keyword, nsize)]

    cursor.execute("""SELECT file FROM find_matches(%s, %s);""", (n_arr, len(n_arr)))
    rows = [[aes.decrypt_string(row[0], session_key, iv), row[0]] for row in cursor.fetchall()]

    return jsonify(files=rows)


@app.route("/file")
def get_file():
    return ""

app.run()
