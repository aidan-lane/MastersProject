from google.cloud import bigquery
from google.oauth2 import service_account
import argparse

if __name__ == "__main__":
    key_path = "service_account.json"

    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)