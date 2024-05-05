import sys

import pytest


def run_tests(*test_args):
    if not test_args:
        test_args = ["tests", "--cov", "--cov-report=xml", "--cov-report=term"]

    retcode: int = pytest.main(test_args)
    sys.exit(retcode)


if __name__ == "__main__":
    run_tests(*sys.argv[1:])
