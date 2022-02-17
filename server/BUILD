load("@python_deps//:requirements.bzl", "requirement")

py_binary(
    name = "run",
    srcs = ["run.py"],
    deps = [
        requirement("google-cloud-bigquery"),
        requirement("google-auth"),
        "//utils:ngrams"
    ]
)