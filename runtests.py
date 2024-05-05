import argparse
import os
import sys

import pytest

DEFAULT_ELASTICSEARCH_URL = "http://localhost:9200"


def make_parser():
    parser = argparse.ArgumentParser(
        prog="Running tests",
        description="Preparing the testing environment and running tests",
    )
    parser.add_argument(
        "--elasticsearch-url",
        action="store",
        default=DEFAULT_ELASTICSEARCH_URL,
        dest="elasticsearch_url",
        metavar="ELASTICSEARCH_URL",
        nargs="?",
        required=False,
        help="For run integration tests with Elasticsearch",
    )
    return parser


def run_tests(*test_args):
    args, test_args = make_parser().parse_known_args(test_args)
    os.environ.setdefault("ELASTICSEARCH_URL", args.elasticsearch_url)

    if not test_args:
        test_args = ["tests", "--cov", "--cov-report=xml", "--cov-report=term"]

    retcode: int = pytest.main(test_args)
    sys.exit(retcode)


if __name__ == "__main__":
    run_tests(*sys.argv[1:])
