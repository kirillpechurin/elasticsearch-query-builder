import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseExistElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.exists = builder_fields.ExistsElasticField(
            field_name="exists_test"
        )
        return cls

    def test_query(self, cls):
        query = cls({"exists": "true"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": "exists_test"
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"exists": "true"}).query
        assert query['query']['bool']['must'][0]['exists']['field'] == "exists_test"

        query = cls({"exists": "false"}).query
        assert query['query']['bool']['must_not'][0]['exists']['field'] == "exists_test"

        query = cls({"exists": "123"}).query
        assert query['query']['bool']['must_not'][0]['exists']['field'] == "exists_test"

    def test_field_name(self, cls):
        query = cls({"exists": "true"}).query
        assert query['query']['bool']['must'][0]['exists']['field'] == "exists_test"

        cls.exists.field_name = "changed_exists_test"

        query = cls({"exists": "true"}).query
        assert query['query']['bool']['must'][0]['exists']['field'] == "changed_exists_test"

    def test_logic_operator(self, cls):
        query = cls({"exists": "true"}).query
        assert query['query']['bool']['must'][0]['exists']['field'] == "exists_test"

        cls.exists._logic_operator = "filter"

        query = cls({"exists": "true"}).query
        assert query['query']['bool']['must'][0]['exists']['field'] == "exists_test"

        cls.exists._logic_operator = "should"

        query = cls({"exists": "true"}).query
        assert query['query']['bool']['must'][0]['exists']['field'] == "exists_test"
