import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseRangeElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.range_field = builder_fields.RangeElasticField(
            field_name="range_field_test",
            lookup_expr="gte",
            input_type=int
        )
        return cls

    def test_query(self, cls):
        query = cls({"range_field": "1"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "range_field_test": {
                                    "gte": 1
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"range_field": "1"}).query
        assert query['query']['bool']['must'][0][
                   'range'
               ]['range_field_test']["gte"] == 1

        query = cls({"range_field": 1}).query
        assert query['query']['bool']['must'][0][
                   'range'
               ]['range_field_test']['gte'] == 1

        query = cls({"range_field": 1.53}).query
        assert query['query']['bool']['must'][0][
                   'range'
               ]['range_field_test']['gte'] == 1

        try:
            query = cls({"range_field": "test-text"}).query
        except ValueError:
            assert True
        else:
            assert False

    def test_field_name(self, cls):
        query = cls({"range_field": "1"}).query
        assert query['query']['bool']['must'][0][
                   'range'
               ]['range_field_test']["gte"] == 1

        cls.range_field.field_name = "changed_range_field_test"

        query = cls({"range_field": "1"}).query
        assert query['query']['bool']['must'][0]['range'] == {
            "changed_range_field_test": {
                "gte": 1
            }
        }

    def test_logic_operator(self, cls):
        query = cls({"range_field": "1"}).query
        assert query['query']['bool']['must'][0][
                   'range'
               ]['range_field_test']["gte"] == 1

        cls.range_field._logic_operator = "filter"

        query = cls({"range_field": "2"}).query
        assert query['query']['bool']['filter'][0][
                   'range'
               ]['range_field_test']["gte"] == 2

        cls.range_field._logic_operator = "should"

        query = cls({"range_field": "3"}).query
        assert query['query']['bool']['should'][0][
                   'range'
               ]['range_field_test']["gte"] == 3

    def test_lookup_expr_gte(self, cls):
        cls.range_field._lookup_expr = "gte"
        query = cls({"range_field": "3"}).query
        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "range_field_test": {
                                    "gte": 3
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_lookup_expr_lte(self, cls):
        cls.range_field._lookup_expr = "lte"
        query = cls({"range_field": "3"}).query
        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "range_field_test": {
                                    "lte": 3
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_lookup_expr_gt(self, cls):
        cls.range_field._lookup_expr = "gt"
        query = cls({"range_field": "3"}).query
        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "range_field_test": {
                                    "gt": 3
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_lookup_expr_lt(self, cls):
        cls.range_field._lookup_expr = "lt"
        query = cls({"range_field": "3"}).query
        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "range_field_test": {
                                    "lt": 3
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_lookup_expr_invalid(self, cls):
        try:
            cls.range_field_2 = builder_fields.RangeElasticField(
                field_name="sample",
                input_type=int,
                lookup_expr="invalid"
            )
        except AssertionError:
            assert True
        else:
            assert False

    def test_input_type_float_validation(self, cls):
        cls.range_field_2 = builder_fields.RangeElasticField(
            field_name="sample",
            input_type=float,
            lookup_expr="gte"
        )

        query = cls({"range_field_2": "1"}).query
        assert query['query']['bool']['must'][0][
                   'range'
               ]['sample']["gte"] == 1.0

        query = cls({"range_field_2": 1}).query
        assert query['query']['bool']['must'][0][
                   'range'
               ]['sample']['gte'] == 1.0

        query = cls({"range_field_2": "1.53"}).query
        assert query['query']['bool']['must'][0][
                   'range'
               ]['sample']['gte'] == 1.53

        try:
            query = cls({"range_field_2": "test-text"}).query
        except ValueError:
            assert True
        else:
            assert False


class TestCaseRangeElasticFieldIntegration:
    index_name = "test_range"
    mappings = {
        "properties": {
            "range_int": {
                "type": "integer"
            },
            "range_float": {
                "type": "float"
            },
            "range_double": {
                "type": "double"
            },
            "range_half_float": {
                "type": "half_float"
            },
            "range_scaled_float": {
                "type": "scaled_float",
                "scaling_factor": 100,
            },
            "nested_range": {
                "type": "nested",
                "properties": {
                    "range_int": {
                        "type": "integer"
                    },
                    "range_float": {
                        "type": "float"
                    },
                }
            }
        }
    }

    @pytest.mark.index_payload(name=index_name, mappings=mappings)
    @pytest.mark.parametrize("builder_params", [
        dict(
            parameter_name="range_int_param",
            field=builder_fields.RangeElasticField(
                field_name="range_int",
                input_type=int,
                lookup_expr="gte"
            ),
            value=123,
        ),
        dict(
            parameter_name="range_float_param",
            field=builder_fields.RangeElasticField(
                field_name="range_float",
                input_type=float,
                lookup_expr="lte"
            ),
            value=123.123,
        ),
        dict(
            parameter_name="range_double_param",
            field=builder_fields.RangeElasticField(
                field_name="range_double",
                input_type=float,
                lookup_expr="gte"
            ),
            value=123.123,
        ),
        dict(
            parameter_name="range_half_float_param",
            field=builder_fields.RangeElasticField(
                field_name="range_half_float",
                input_type=float,
                lookup_expr="gte"
            ),
            value=123.123,
        ),
        dict(
            parameter_name="range_scaled_float_param",
            field=builder_fields.RangeElasticField(
                field_name="range_scaled_float",
                input_type=float,
                lookup_expr="gte"
            ),
            value=123.12,
        ),
        dict(
            parameter_name="nested_range_param",
            field=builder_fields.NestedElasticField(
                path="nested_range",
                child=builder_fields.RangeElasticField(
                    field_name="range_int",
                    input_type=int,
                    lookup_expr="gte"
                ),
            ),
            value=123.123,
        ),
        dict(
            parameter_name="nested_range_param",
            field=builder_fields.NestedElasticField(
                path="nested_range",
                child=builder_fields.RangeElasticField(
                    field_name="range_float",
                    input_type=float,
                    lookup_expr="lte"
                ),
            ),
            value=123.123,
        ),
    ])
    def test_request(self,
                     elasticsearch_client,
                     make_builder_instance,
                     builder_params):
        query = make_builder_instance(builder_params).query
        data = elasticsearch_client.search(index=self.index_name, **query)
        assert isinstance(data, dict)
        assert data.get("hits") is not None
        assert data["hits"]["total"]["value"] == 0
