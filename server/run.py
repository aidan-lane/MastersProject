import sys
import argparse

from google.cloud import bigquery
from google.cloud import storage
from google.oauth2 import service_account

import utils


##############################
# Google Cloud Clients Setup #
##############################

# Credentials
key_path = "server/service_account.json"
credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# BigQuery
bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

# Cloud Storage
storage_client = storage.Client(credentials=credentials, 
    project=credentials.project_id,)
bucket = "al-enc-files"


def parse_args():
    """ 
    Parses command line arguments and returns set or default values.
    Returns tuple with ngram size and scheme type
    """
    parser = argparse.ArgumentParser(description="Server parameters")
    parser.add_argument("--ngrams", type=int, help="Length of each individual ngram. \
        Default is 3", default=3)
    parser.add_argument("--scheme", type=str, help="What encryption/decryption to use. \
        Default is AES64", default="AES64")
    args = parser.parse_args()

    return args.ngrams, args.scheme


def help_menu(args):
    print("--------------------------")
    print("Commands:")
    for command in commands.keys():
        print("\"{}\": {}".format(command, commands[command][1]))
    print("--------------------------")


def upload(args):
    if len(args) != 2:
        print("Invalid number of arguments, should be: [file] [keywords]")
        return

    filepath = args[0]
    keywords = args[1].split(",")

    # Encrypt and upload file
    utils.aes.generate_key()


commands = {
    "quit": (lambda _: sys.exit(0), "Quit the application"),
    "help": (help_menu, "List of valid commands and their descriptions"),
    "upload": (upload, "Uploads the given file with comma-deliminated keywords.\n\tExample: upload test.txt k1,k2")
}


if __name__ == "__main__":

    ngrams, sceheme = parse_args()

    ###########################
    # User Command Processing #
    ###########################

    print("Enter command:")
    command = ""
    while command != "quit":
        command, *args = input().lower().split(" ")

        if command in commands:
            commands[command][0](args)
        else:
            print("Unknown command! Type help for a list of available command")