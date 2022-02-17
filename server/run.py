from google.cloud import bigquery
from google.oauth2 import service_account
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Server parameters")
    parser.add_argument("--ngrams", type=int, help="Length of each individual ngram. \
        Default is 3", default=3)
    parser.add_argument("--scheme", type=str, help="What encryption/decryption to use. \
        Default is AES64", default="AES64")
    args = parser.parse_args()

    ngrams = args.ngrams
    scheme = args.scheme

    key_path = "service_account.json"
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)