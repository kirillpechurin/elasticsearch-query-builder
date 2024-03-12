import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseMatchPhrasePrefixElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.match_phrase_prefix = builder_fields.MatchPhrasePrefixElasticField(
            field_name="test_field"
        )
        return cls

    def test_query(self, cls):
        query = cls({"match_phrase_prefix": "test_text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase_prefix": {
                                "test_field": {
                                    "query": "test_text"
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"match_phrase_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0]['match_phrase_prefix']['test_field']["query"] == "test_text"

        query = cls({"match_phrase_prefix": "test"}).query
        assert query['query']['bool']['must'][0]['match_phrase_prefix']['test_field']['query'] == "test"

        query = cls({"match_phrase_prefix": "test text"}).query
        assert query['query']['bool']['must'][0]['match_phrase_prefix']['test_field']['query'] == 'test text'

    def test_field_name(self, cls):
        query = cls({"match_phrase_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0]['match_phrase_prefix']['test_field']["query"] == "test_text"

        cls.match_phrase_prefix.field_name = "changed_test_field"

        query = cls({"match_phrase_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0]['match_phrase_prefix']['changed_test_field']["query"] == "test_text"

    def test_logic_operator(self, cls):
        query = cls({"match_phrase_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0]['match_phrase_prefix']['test_field']["query"] == "test_text"

        cls.match_phrase_prefix._logic_operator = "filter"

        query = cls({"match_phrase_prefix": "test_text"}).query
        assert query['query']['bool']['filter'][0]['match_phrase_prefix']['test_field']["query"] == "test_text"

        cls.match_phrase_prefix._logic_operator = "should"

        query = cls({"match_phrase_prefix": "test_text"}).query
        assert query['query']['bool']['should'][0]['match_phrase_prefix']['test_field']["query"] == "test_text"
