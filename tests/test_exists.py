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


class TestCaseExistElasticFieldIntegration:
    index_name = "test_exists"
    mappings = {
        "properties": {
            "exists_test": {
                "type": "integer"
            },
            "nested_exists": {
                "type": "nested",
                "properties": {
                    "exists_test": {
                        "type": "integer"
                    },
                }
            }
        }
    }

    @pytest.mark.index_payload(name=index_name, mappings=mappings)
    @pytest.mark.parametrize("builder_params", [
        dict(
            parameter_name="exists_param",
            field=builder_fields.ExistsElasticField(
                field_name="exists_test"
            ),
            value=True,
        ),
        dict(
            parameter_name="exists_param",
            field=builder_fields.ExistsElasticField(
                field_name="exists_test"
            ),
            value=False,
        ),
        dict(
            parameter_name="nested_exists_param",
            field=builder_fields.NestedElasticField(
                path="nested_exists",
                child=builder_fields.ExistsElasticField(
                    field_name="exists_test"
                )
            ),
            value="true",
        ),
        dict(
            parameter_name="nested_exists_param",
            field=builder_fields.NestedElasticField(
                path="nested_exists",
                child=builder_fields.ExistsElasticField(
                    field_name="exists_test"
                )
            ),
            value="false",
        ),
    ])
    def test_request(self, elasticsearch_client, make_builder_instance, builder_params):
        query = make_builder_instance(builder_params).query
        data = elasticsearch_client.search(index=self.index_name, **query)
        assert isinstance(data, dict)
        assert data.get("hits") is not None
        assert data["hits"]["total"]["value"] == 0
