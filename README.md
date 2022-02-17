# Fuzzy Search on Encrypted Data in the Cloud
Master Thesis Project 2022

## Server console setup
1. Add project associated `service_account.json` secret to project directory.
2. Build server target with `bazel build //server:run`
3. Run with `./bazel-bin/server/run [args]`
    - ngram: Size of ngrams (default 3)
    - scheme: Encryption scheme to encrypt files and ngrams (AES, Base64)

Example run usage:
`./bazel-bin/server/run ngram=3 scheme=AES`
***
## Web Application Startup
See `/application` directory for details



