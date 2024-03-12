import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseMatchPhraseElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.match_phrase = builder_fields.MatchPhraseElasticField(
            field_name="test_field"
        )
        return cls

    def test_query(self, cls):
        query = cls({"match_phrase": "test_text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase": {
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
        query = cls({"match_phrase": "test_text"}).query
        assert query['query']['bool']['must'][0]['match_phrase']['test_field']["query"] == "test_text"

        query = cls({"match_phrase": "test"}).query
        assert query['query']['bool']['must'][0]['match_phrase']['test_field']['query'] == "test"

        query = cls({"match_phrase": "test text"}).query
        assert query['query']['bool']['must'][0]['match_phrase']['test_field']['query'] == 'test text'

    def test_field_name(self, cls):
        query = cls({"match_phrase": "test_text"}).query
        assert query['query']['bool']['must'][0]['match_phrase']['test_field']["query"] == "test_text"

        cls.match_phrase.field_name = "changed_test_field"

        query = cls({"match_phrase": "test_text"}).query
        assert query['query']['bool']['must'][0]['match_phrase']['changed_test_field']["query"] == "test_text"

    def test_logic_operator(self, cls):
        query = cls({"match_phrase": "test_text"}).query
        assert query['query']['bool']['must'][0]['match_phrase']['test_field']["query"] == "test_text"

        cls.match_phrase._logic_operator = "filter"

        query = cls({"match_phrase": "test_text"}).query
        assert query['query']['bool']['filter'][0]['match_phrase']['test_field']["query"] == "test_text"

        cls.match_phrase._logic_operator = "should"

        query = cls({"match_phrase": "test_text"}).query
        assert query['query']['bool']['should'][0]['match_phrase']['test_field']["query"] == "test_text"
