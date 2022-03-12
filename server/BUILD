load("@python_deps//:requirements.bzl", "requirement")

py_binary(
    name = "run",
    srcs = ["run.py"],
    deps = [
        requirement("google-cloud-bigquery"),
        requirement("google-cloud-storage"),
        requirement("google-auth"),
        requirement("pycrypto"),
        "//utils:aes",
        "//utils:ngrams"
    ],
    data = [
        "service_account.json"
    ]
)