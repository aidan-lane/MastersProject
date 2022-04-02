load("@python_deps//:requirements.bzl", "requirement")

py_binary(
    name = "run",
    srcs = ["run.py"],
    deps = [
        requirement("google-cloud-storage"),
        requirement("google-auth"),
        requirement("psycopg2-binary"),
        requirement("python-dotenv"),
        "//utils:aes",
        "//utils:ngrams"
    ],
    data = [
        "service_account.json",
        ".env"
    ]
)