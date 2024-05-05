import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseMatchBoolPrefixElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.match_bool_prefix = builder_fields.MatchBoolPrefixElasticField(
            field_name="test_field"
        )
        return cls

    def test_query(self, cls):
        query = cls({"match_bool_prefix": "test_text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_bool_prefix": {
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
        query = cls({"match_bool_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0][
                   'match_bool_prefix'
               ]['test_field']["query"] == "test_text"

        query = cls({"match_bool_prefix": "test"}).query
        assert query['query']['bool']['must'][0][
                   'match_bool_prefix'
               ]['test_field']['query'] == "test"

        query = cls({"match_bool_prefix": "test text"}).query
        assert query['query']['bool']['must'][0][
                   'match_bool_prefix'
               ]['test_field']['query'] == 'test text'

    def test_field_name(self, cls):
        query = cls({"match_bool_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0][
                   'match_bool_prefix'
               ]['test_field']["query"] == "test_text"

        cls.match_bool_prefix.field_name = "changed_test_field"

        query = cls({"match_bool_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0][
                   'match_bool_prefix'
               ]['changed_test_field']["query"] == "test_text"

    def test_logic_operator(self, cls):
        query = cls({"match_bool_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0][
                   'match_bool_prefix'
               ]['test_field']["query"] == "test_text"

        cls.match_bool_prefix._logic_operator = "filter"

        query = cls({"match_bool_prefix": "test_text"}).query
        assert query['query']['bool']['filter'][0][
                   'match_bool_prefix'
               ]['test_field']["query"] == "test_text"

        cls.match_bool_prefix._logic_operator = "should"

        query = cls({"match_bool_prefix": "test_text"}).query
        assert query['query']['bool']['should'][0][
                   'match_bool_prefix'
               ]['test_field']["query"] == "test_text"

    def test_default_attrs(self, cls):
        assert cls.match_bool_prefix._attrs == [
            ("operator", None),
            ("minimum_should_match", None),
        ]

    def test_attr_operator(self, cls):
        cls.match_bool_prefix._attrs = [
            ("operator", "AND"),
            ("fuzziness", None),
            ("minimum_should_match", None),
        ]

        query = cls({"match_bool_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0][
                   'match_bool_prefix'
               ]['test_field'] == {
                   "query": "test_text",
                   "operator": "AND"
               }

    def test_attr_minimum_should_match(self, cls):
        cls.match_bool_prefix._attrs = [
            ("operator", None),
            ("minimum_should_match", "85%"),
        ]

        query = cls({"match_bool_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0][
                   'match_bool_prefix'
               ]['test_field'] == {
                   "query": "test_text",
                   "minimum_should_match": "85%"
               }

    def test_all_attrs(self, cls):
        cls.match_bool_prefix._attrs = [
            ("operator", "AND"),
            ("minimum_should_match", "85%"),
        ]

        query = cls({"match_bool_prefix": "test_text"}).query
        assert query['query']['bool']['must'][0][
                   'match_bool_prefix'
               ]['test_field'] == {
                   "query": "test_text",
                   "operator": "AND",
                   "minimum_should_match": "85%"
               }


class TestCaseMatchBoolPrefixElasticFieldIntegration:
    index_name = "test_match_bool_prefix"
    mappings = {
        "properties": {
            "match_bool_prefix_text": {
                "type": "text"
            },
            "nested_match_bool_prefix": {
                "type": "nested",
                "properties": {
                    "match_bool_prefix_text": {
                        "type": "text"
                    },
                }
            }
        }
    }

    @pytest.mark.index_payload(name=index_name, mappings=mappings)
    @pytest.mark.parametrize("builder_params", [
        dict(
            parameter_name="match_bool_prefix_param",
            field=builder_fields.MatchBoolPrefixElasticField(
                field_name="match_bool_prefix_text",
                operator="AND",
                minimum_should_match="85%"
            ),
            value="sample text",
        ),
        dict(
            parameter_name="nested_match_bool_prefix_param",
            field=builder_fields.NestedElasticField(
                path="nested_match_bool_prefix",
                child=builder_fields.MatchBoolPrefixElasticField(
                    field_name="match_bool_prefix_text",
                    operator="AND",
                    minimum_should_match="85%"
                ),
            ),
            value="sample text",
        ),
    ])
    def test_request(self,
                     elasticsearch_client,
                     make_builder_instance,
                     builder_params):
        query = make_builder_instance(builder_params).query
        data = elasticsearch_client.search(index=self.index_name, **query)
        assert data["hits"] is not None
        assert data["hits"]["total"]["value"] == 0
