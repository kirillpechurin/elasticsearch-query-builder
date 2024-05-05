import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseMatchElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.query_string_field = builder_fields.QueryStringElasticField(
            field_name="query_string_field_test"
        )
        return cls

    def test_query(self, cls):
        query = cls({"query_string_field": "test-text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "query": "test-text",
                                "default_field": "query_string_field_test"
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0][
                   'query_string'
               ]["query"] == "test-text"

        query = cls({"query_string_field": "[1, 2, 3]"}).query
        assert query['query']['bool']['must'][0][
                   'query_string'
               ]['query'] == "[1, 2, 3]"

        query = cls({"query_string_field": 1.53}).query
        assert query['query']['bool']['must'][0][
                   'query_string'
               ]['query'] == "1.53"

    def test_field_name(self, cls):
        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0][
                   'query_string'
               ]["query"] == "test-text"

        cls.query_string_field.field_name = "changed_query_string_field_test"

        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0][
                   'query_string'
               ] == {
            "query": "test-text",
            "default_field": "query_string_field_test"
        }

    def test_logic_operator(self, cls):
        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0][
                   'query_string'
               ]["query"] == "test-text"

        cls.query_string_field._logic_operator = "filter"

        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['filter'][0][
                   'query_string'
               ]["query"] == "test-text"

        cls.query_string_field._logic_operator = "should"

        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['should'][0][
                   'query_string'
               ]["query"] == "test-text"

    def test_default_attrs(self, cls):
        assert cls.query_string_field._attrs == [
            ("fuzziness", None),
            ("default_operator", None),
            ("minimum_should_match", None),
            ("default_field", "query_string_field_test"),
        ]

    def test_default_attrs_with_fields(self, cls):
        cls.query_string_field_2 = builder_fields.QueryStringElasticField(
            fields=["sample_1", "sample_2"]
        )
        assert cls.query_string_field_2._attrs == [
            ("fuzziness", None),
            ("default_operator", None),
            ("minimum_should_match", None),
            ("fields", ["sample_1", "sample_2"]),
        ]

    def test_attr_fuzziness(self, cls):
        cls.query_string_field._attrs = [
            ("fuzziness", "auto"),
            ("default_operator", None),
            ("minimum_should_match", None),
            ("default_field", "query_string_field_test"),
        ]

        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['query_string'] == {
            "query": "test-text",
            "fuzziness": "auto",
            "default_field": "query_string_field_test"
        }

    def test_attr_default_operator(self, cls):
        cls.query_string_field._attrs = [
            ("fuzziness", None),
            ("default_operator", "AND"),
            ("minimum_should_match", None),
            ("default_field", "query_string_field_test"),
        ]

        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['query_string'] == {
            "query": "test-text",
            "default_operator": "AND",
            "default_field": "query_string_field_test"
        }

    def test_attr_minimum_should_match(self, cls):
        cls.query_string_field._attrs = [
            ("fuzziness", None),
            ("default_operator", None),
            ("minimum_should_match", "85%"),
            ("default_field", "query_string_field_test"),
        ]

        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['query_string'] == {
            "query": "test-text",
            "minimum_should_match": "85%",
            "default_field": "query_string_field_test"
        }

    def test_attr_default_field(self, cls):
        cls.query_string_field._attrs = [
            ("fuzziness", None),
            ("default_operator", None),
            ("minimum_should_match", None),
            ("default_field", "sample"),
        ]

        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['query_string'] == {
            "query": "test-text",
            "default_field": "sample"
        }

    def test_attr_fields(self, cls):
        cls.query_string_field._attrs = [
            ("fuzziness", None),
            ("default_operator", None),
            ("minimum_should_match", None),
            ("fields", ["sample_1", "sample_2"]),
        ]

        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['query_string'] == {
            "query": "test-text",
            "fields": ["sample_1", "sample_2"]
        }

    def test_all_attrs_with_default_field(self, cls):
        cls.query_string_field._attrs = [
            ("fuzziness", "auto"),
            ("default_operator", "AND"),
            ("minimum_should_match", "85%"),
            ("default_field", "sample"),
        ]

        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['query_string'] == {
            "query": "test-text",
            "fuzziness": "auto",
            "default_operator": "AND",
            "minimum_should_match": "85%",
            "default_field": "sample"
        }

    def test_all_attrs_with_fields(self, cls):
        cls.query_string_field._attrs = [
            ("fuzziness", "auto"),
            ("default_operator", "AND"),
            ("minimum_should_match", "85%"),
            ("fields", ["sample_1", "sample_2"]),
        ]

        query = cls({"query_string_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['query_string'] == {
            "query": "test-text",
            "fuzziness": "auto",
            "default_operator": "AND",
            "minimum_should_match": "85%",
            "fields": ["sample_1", "sample_2"]
        }


class TestCaseQueryStringElasticFieldIntegration:
    index_name = "test_query_string"
    mappings = {
        "properties": {
            "query_string_text_1": {
                "type": "text"
            },
            "query_string_text_2": {
                "type": "text"
            },
            "nested_query_string": {
                "type": "nested",
                "properties": {
                    "query_string_text_1": {
                        "type": "text"
                    },
                    "query_string_text_2": {
                        "type": "text"
                    },
                }
            }
        }
    }

    @pytest.mark.index_payload(name=index_name, mappings=mappings)
    @pytest.mark.parametrize("builder_params", [
        dict(
            parameter_name="query_string_param",
            field=builder_fields.QueryStringElasticField(
                default_field="query_string_text_1",
                fuzziness="auto",
                default_operator="AND",
                minimum_should_match="85%"
            ),
            value="sample text",
        ),
        dict(
            parameter_name="query_string_param",
            field=builder_fields.QueryStringElasticField(
                fields=[
                    "query_string_text_1",
                    "query_string_text_2"
                ],
                fuzziness="auto",
                default_operator="AND",
                minimum_should_match="85%"
            ),
            value="sample text",
        ),
        dict(
            parameter_name="query_string_param",
            field=builder_fields.QueryStringElasticField(
                field_name="query_string_text_1",
                fuzziness="auto",
                default_operator="AND",
                minimum_should_match="85%"
            ),
            value="sample text",
        ),
        dict(
            parameter_name="nested_query_string_param",
            field=builder_fields.NestedElasticField(
                path="nested_query_string",
                child=builder_fields.QueryStringElasticField(
                    default_field="query_string_text",
                    fuzziness="auto",
                    default_operator="AND",
                    minimum_should_match="85%"
                ),
            ),
            value="sample text",
        ),
        dict(
            parameter_name="nested_query_string_param",
            field=builder_fields.NestedElasticField(
                path="nested_query_string",
                child=builder_fields.QueryStringElasticField(
                    fields=[
                        "query_string_text_1",
                        "query_string_text_2"
                    ],
                    fuzziness="auto",
                    default_operator="AND",
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
