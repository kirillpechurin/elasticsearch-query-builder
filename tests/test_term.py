import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseTermElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.term_field = builder_fields.TermElasticField(
            field_name="term_field_test",
            input_type=int
        )
        return cls

    def test_query(self, cls):
        query = cls({"term_field": "1"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "term_field_test": 1
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"term_field": "1"}).query
        assert query['query']['bool']['must'][0]['term']['term_field_test'] == 1

        query = cls({"term_field": 1}).query
        assert query['query']['bool']['must'][0]['term']['term_field_test'] == 1

        query = cls({"term_field": 1.53}).query
        assert query['query']['bool']['must'][0]['term']['term_field_test'] == 1

        try:
            query = cls({"term_field": "test-text"}).query
        except ValueError:
            assert True
        else:
            assert False

    def test_field_name(self, cls):
        query = cls({"term_field": "1"}).query
        assert query['query']['bool']['must'][0]['term']['term_field_test'] == 1

        cls.term_field.field_name = "changed_term_field_test"

        query = cls({"term_field": "1"}).query
        assert query['query']['bool']['must'][0]['term'] == {
            "changed_term_field_test": 1
        }

    def test_logic_operator(self, cls):
        query = cls({"term_field": "1"}).query
        assert query['query']['bool']['must'][0]['term']['term_field_test'] == 1

        cls.term_field._logic_operator = "filter"

        query = cls({"term_field": "2"}).query
        assert query['query']['bool']['filter'][0]['term']['term_field_test'] == 2

        cls.term_field._logic_operator = "should"

        query = cls({"term_field": "3"}).query
        assert query['query']['bool']['should'][0]['term']['term_field_test'] == 3

    def test_input_type_bool_validation(self, cls):
        cls.term_field_2 = builder_fields.TermElasticField(
            field_name="sample",
            input_type=bool,
        )

        query = cls({"term_field_2": "true"}).query
        assert query['query']['bool']['must'][0]['term']['sample'] is True

        query = cls({"term_field_2": "any"}).query
        assert query['query']['bool']['must'][0]['term']['sample'] is False

        query = cls({"term_field_2": True}).query
        assert query['query']['bool']['must'][0]['term']['sample'] is True

        query = cls({"term_field_2": False}).query
        assert query['query']['bool']['must'][0]['term']['sample'] is False

        query = cls({"term_field_2": "test-text"}).query
        assert query['query']['bool']['must'][0]['term']['sample'] is False

    def test_input_type_str_validation(self, cls):
        cls.term_field_2 = builder_fields.TermElasticField(
            field_name="sample",
            input_type=str,
        )

        query = cls({"term_field_2": "1"}).query
        assert query['query']['bool']['must'][0]['term']['sample'] == "1"

        query = cls({"term_field_2": 1}).query
        assert query['query']['bool']['must'][0]['term']['sample'] == "1"

        query = cls({"term_field_2": "1.53"}).query
        assert query['query']['bool']['must'][0]['term']['sample'] == "1.53"

        query = cls({"term_field_2": "test-text"}).query
        assert query['query']['bool']['must'][0]['term']['sample'] == "test-text"
