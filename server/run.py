import os
import argparse
import cmd

from google.oauth2 import service_account
import psycopg2 as sql
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from google.cloud import storage

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
load_dotenv()
conn = sql.connect(database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASS"), host=os.getenv("DB_HOST"))
cursor = conn.cursor()

###################
# Private AES Key #
###################

private_key = aes.generate_key()


def parse_args():
    """ 
    Parses command line arguments and returns set or default values.
    Returns tuple with ngram size and scheme type
    """
    parser = argparse.ArgumentParser(description="Server parameters")
    parser.add_argument("files", type=str, help="Path to folder that contains files that can be uploaded.")
    parser.add_argument("--ngram_size", type=int, help="Length of each individual ngram. \
        Default is 3", default=3)
    args = parser.parse_args()

    return args.files, args.ngram_size


def init_db():
    query = """
        CREATE TABLE IF NOT EXISTS ngrams (
            efile TEXT NOT NULL,
            keynum INTEGER NOT NULL,
            ngram TEXT NOT NULL,
            PRIMARY KEY (ngram, keynum, efile)
        );

        CREATE OR REPLACE FUNCTION find_matches(TEXT[], INT) 
        RETURNS TABLE(file TEXT, score decimal)
        AS $$ 
            SELECT n.efile, cast(COUNT(n.ngram) as decimal) / $2 score
            FROM UNNEST($1) elem 
            JOIN ngrams n ON n.ngram = elem
            GROUP BY n.efile, n.keynum
            SORT BY score DESC
        $$
        LANGUAGE SQL;
    """
    cursor.execute(query)
    conn.commit()


class AppShell(cmd.Cmd):
    prompt = ">>> "
    intro = "Type help or ? to list commands.\n"

    def __init__(self, abspath, ngram_size):
        super(AppShell, self).__init__()

        self.abspath = abspath
        self.ngram_size = ngram_size

    def precmd(self, line):
        return line.lower().strip()

    def do_quit(self, _):
        "Exits the application"
        return True

    def do_author(self, _):
        "Prints author and related information for this project"
        print("Aidan Lane, lanea3@rpi.edu")

    def do_upload(self, args):
        "Uploads the given file in specified absolute 'files' path with co" \
            "mma-deliminated keywords.\nExample: upload file.txt k1,k2"
        parser = argparse.ArgumentParser(description="Encrypt and upload file to Google Cloud Storage", 
            usage="upload file.txt key1,key2")
        parser.add_argument("file", type=str, help="File to be uploaded to the cloud")
        parser.add_argument("keywords", type=str, help="Plaintext keywords associated with file")

        try:
            args = parser.parse_args(args.split(" "))
        except SystemExit:
            return

        filename = args.file
        keywords = args.keywords.split(",")

        # Encrypt file
        out_path = aes.encrypt_file(private_key, os.path.join(self.abspath, filename))
        # Obscure file name by encoding it
        encfile = aes.encrypt_string(os.path.basename(filename))

        # Lookup or create bucket if it doesn't exist
        file_bucket = storage_client.lookup_bucket(file_bucket_name)
        if not file_bucket:
            file_bucket = storage_client.create_bucket(file_bucket_name)

        blob = file_bucket.blob(encfile)
        blob.upload_from_filename(out_path)

        # # Generate n-grams and send to database
        insert_query = """
            INSERT INTO ngrams (efile, keynum, ngram) VALUES %s ON CONFLICT DO NOTHING;
        """

        data = []
        for i, keyword in enumerate(keywords):
            for ngram in ngrams.extract_ngrams(keyword, self.ngram_size):
                data.append((encfile, i, ngram))

        execute_values(cursor, insert_query, data)
        conn.commit()
        print("Inserted {} ngrams into ngrams table".format(cursor.rowcount))

    
    def do_delete_all(self, _):
        "Deletes all ngrams from the database"
        delete_query = """
            DELETE FROM ngrams;
        """
        cursor.execute(delete_query)
        conn.commit()
        print("Deleted {} rows from ngrams table".format(cursor.rowcount))


if __name__ == "__main__":
    # Command line argument parsing
    abspath, ngram_size = parse_args()

    # Intialize Database
    init_db()

    # Application command parsing
    shell = AppShell(abspath, ngram_size)
    while True:
        try:
            print()
            shell.cmdloop()
            break
        except KeyboardInterrupt:
            pass
