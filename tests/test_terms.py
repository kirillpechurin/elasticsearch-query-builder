import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseTermsElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.terms_field = builder_fields.TermsElasticField(
            field_name="terms_field_tests"
        )
        return cls

    def test_query(self, cls):
        query = cls({"terms_field": [1, 2, 3, 4]}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "terms": {
                                "terms_field_tests": [1, 2, 3, 4]
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"terms_field": (i for i in range(1, 3 + 1))}).query
        assert query['query']['bool']['must'][0]['terms']["terms_field_tests"] == [1, 2, 3]

        query = cls({"terms_field": tuple(i for i in range(1, 3 + 1))}).query
        assert query['query']['bool']['must'][0]['terms']["terms_field_tests"] == [1, 2, 3]

        class _IterableExample:

            def __init__(self, start, end):
                self._start = start
                self._end = end
                self._current = self._start

            def __iter__(self):
                return self

            def __next__(self):
                if self._current >= self._end:
                    raise StopIteration
                self._current += 1
                return self._current - 1

        query = cls({"terms_field": _IterableExample(1, 5)}).query
        assert query['query']['bool']['must'][0]['terms']["terms_field_tests"] == [1, 2, 3, 4]

    def test_field_name(self, cls):
        query = cls({"terms_field": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0]['terms']["terms_field_tests"] == [1, 2, 3]

        cls.terms_field.field_name = "changed_terms_field"

        query = cls({"terms_field": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0]['terms']["changed_terms_field"] == [1, 2, 3]

    def test_logic_operator(self, cls):
        query = cls({"terms_field": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0]['terms']["terms_field_tests"] == [1, 2, 3]

        cls.terms_field._logic_operator = "filter"

        query = cls({"terms_field": [1, 2, 3]}).query
        assert query['query']['bool']['filter'][0]['terms']["terms_field_tests"] == [1, 2, 3]

        cls.terms_field._logic_operator = "should"

        query = cls({"terms_field": [1, 2, 3]}).query
        assert query['query']['bool']['should'][0]['terms']["terms_field_tests"] == [1, 2, 3]


class TestCaseTermsElasticFieldIntegration:
    index_name = "test_terms"
    mappings = {
        "properties": {
            "terms_int": {
                "type": "integer"
            },
            "terms_text": {
                "type": "text"
            },
            "nested_terms": {
                "type": "nested",
                "properties": {
                    "terms_int": {
                        "type": "integer"
                    },
                    "terms_text": {
                        "type": "text"
                    },
                }
            },
        }
    }

    @pytest.mark.index_payload(name=index_name, mappings=mappings)
    @pytest.mark.parametrize("builder_params", [
        dict(
            parameter_name="terms_int_param",
            field=builder_fields.TermsElasticField(
                field_name="terms_int"
            ),
            value=[1, 2, 3],
        ),
        dict(
            parameter_name="terms_text_param",
            field=builder_fields.TermsElasticField(
                field_name="terms_text"
            ),
            value=["sample-1", "sample-2", "sample-3"],
        ),
        dict(
            parameter_name="nested_terms_int_param",
            field=builder_fields.NestedElasticField(
                path="nested_terms",
                child=builder_fields.TermsElasticField(
                    field_name="terms_int",
                )
            ),
            value=[1, 2, 3],
        ),
        dict(
            parameter_name="nested_terms_text_param",
            field=builder_fields.NestedElasticField(
                path="nested_terms",
                child=builder_fields.TermsElasticField(
                    field_name="terms_text",
                )
            ),
            value=["sample-1", "sample-2", "sample-3"],
        ),
    ])
    def test_request(self, elasticsearch_client, make_builder_instance, builder_params):
        query = make_builder_instance(builder_params).query
        data = elasticsearch_client.search(index=self.index_name, **query)
        assert isinstance(data, dict)
        assert data.get("hits") is not None
        assert data["hits"]["total"]["value"] == 0
