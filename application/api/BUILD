load("@python_deps//:requirements.bzl", "requirement")

py_library(
    name = "session",
    srcs = ["session.py"],
    visibility = ["//application:__subpackages__"]
)

py_binary(
    name = "backend",
    srcs = ["backend.py"],
    deps = [
        "session",
        requirement("google-cloud-storage"),
        requirement("google-auth"),
        requirement("psycopg2-binary"),
        requirement("python-dotenv"),
        "//utils:aes",
        "//utils:ngrams"
    ],
    data = [
        "//server:service_account.json",
        "//server:.env"
    ]
)