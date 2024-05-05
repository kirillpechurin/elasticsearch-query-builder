import os

import dotenv
import pytest
from elasticsearch import Elasticsearch

from .builder import ElasticSearchQueryTestBuilder

dotenv.load_dotenv("./.env")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "index_payload: mark test to run with prepared index"
    )
    os.environ.setdefault("ELASTICSEARCH_URL", "http://localhost:9200")
    os.environ.setdefault("ELASTICSEARCH_USERNAME", "elastic")
    os.environ.setdefault("ELASTICSEARCH_PASSWORD", "changeme")


@pytest.fixture
def elasticsearch_client(request):
    client = Elasticsearch(
        os.environ["ELASTICSEARCH_URL"],
        http_auth=(
            os.environ["ELASTICSEARCH_USERNAME"],
            os.environ["ELASTICSEARCH_PASSWORD"]
        )
    )

    index_payload = request.node.get_closest_marker("index_payload")
    if index_payload:
        client.indices.delete(index=index_payload.kwargs["name"], ignore=[404])
        client.indices.create(
            index=index_payload.kwargs["name"],
            mappings=index_payload.kwargs["mappings"]
        )

    yield client

    if index_payload:
        client.indices.delete(index=index_payload.kwargs["name"])

    client.close()


@pytest.fixture
def make_builder():
    def _make_builder(builder_params):
        builder = ElasticSearchQueryTestBuilder
        setattr(
            builder,
            builder_params["parameter_name"],
            builder_params["field"]
        )
        return builder

    return _make_builder


@pytest.fixture
def make_builder_instance(make_builder):
    def _make_builder_instance(builder_params):
        return make_builder(builder_params)({
            builder_params["parameter_name"]: builder_params["value"]
        })

    return _make_builder_instance
