load("@python_deps//:requirements.bzl", "requirement")

py_library(
    name = "aes",
    srcs = ["aes.py"],
    deps = [requirement("pycryptodome")],
    visibility = ["//visibility:public"]
)

py_library(
    name = "ngrams",
    srcs = ["ngrams.py"],
    visibility = ["//visibility:public"]
)

py_test(
    name = "aes_test",
    srcs = ["aes_test.py"],
    deps = ["//utils:aes"]
)

py_test(
    name = "ngrams_test",
    srcs = ["ngrams_test.py"],
    deps = ["//utils:ngrams"]
)