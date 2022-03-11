load("@python_deps//:requirements.bzl", "requirement")

py_library(
    name = "utils",
    srcs = ["ngrams.py", "aes.py"],
    deps = [requirement("pycrypto")],
    visibility = ["//server:__subpackages__"]
)

py_test(
    name = "ngrams_test",
    srcs = ["ngrams_test.py"]
)