import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseNestedElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.nested_field = builder_fields.NestedElasticField(
            path="rootpath",
            child=builder_fields.MatchElasticField(
                field_name="match_test_field",
                input_type=str
            )
        )
        return cls

    def test_query(self, cls):
        query = cls({"nested_field": "test-text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "nested": {
                                "path": "rootpath",
                                "query": {
                                    "match": {
                                        "rootpath.match_test_field": {
                                            "query": "test-text"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_child_validation(self, cls):
        query = cls({"nested_field": "1"}).query
        assert query['query']['bool']['must'][0]["nested"]["query"]['match'][
                   "rootpath.match_test_field"
               ]["query"] == "1"

        query = cls({"nested_field": "test-text"}).query
        assert query['query']['bool']['must'][0]["nested"]["query"]['match'][
                   "rootpath.match_test_field"
               ]["query"] == "test-text"

        cls.nested_field._child._input_type = int
        query = cls({"nested_field": "1"}).query
        assert query['query']['bool']['must'][0]["nested"]["query"]['match'][
                   "rootpath.match_test_field"
               ]["query"] == 1

    def test_path(self, cls):
        query = cls({"nested_field": "test-text"}).query
        assert query['query']['bool']['must'][0]["nested"]["query"]['match'][
                   "rootpath.match_test_field"
               ]["query"] == "test-text"

        cls.nested_field._path = "changed_rootpath"

        query = cls({"nested_field": "test-text"}).query
        assert query['query']['bool']['must'][0]["nested"] == {
            "path": "changed_rootpath",
            "query": {
                "match": {
                    "changed_rootpath.match_test_field": {
                        "query": "test-text"
                    }
                }
            }
        }

    def test_field_name(self, cls):
        query = cls({"nested_field": "test-text"}).query
        assert query['query']['bool']['must'][0]["nested"]["query"]['match'][
                   "rootpath.match_test_field"
               ]["query"] == "test-text"

        cls.nested_field._child.field_name = "changed_child_field_name"

        query = cls({"nested_field": "test-text"}).query
        assert query['query']['bool']['must'][0]["nested"]["query"]['match'][
                   "rootpath.changed_child_field_name"
               ]["query"] == "test-text"
