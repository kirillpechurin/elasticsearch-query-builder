import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseIdsElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.ids = builder_fields.IdsElasticField(
            field_name="ids_test"
        )
        return cls

    def test_query(self, cls):
        query = cls({"ids": [1, 2, 3, 4]}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "ids": {
                                "values": [1, 2, 3, 4]
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"ids": (i for i in range(1, 3 + 1))}).query
        assert query['query']['bool']['must'][0]['ids']["values"] == [1, 2, 3]

        query = cls({"ids": tuple(i for i in range(1, 3 + 1))}).query
        assert query['query']['bool']['must'][0]['ids']["values"] == [1, 2, 3]

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

        query = cls({"ids": _IterableExample(1, 5)}).query
        assert query['query']['bool']['must'][0][
                   'ids'
               ]["values"] == [1, 2, 3, 4]

    def test_field_name(self, cls):
        query = cls({"ids": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0][
                   'ids'
               ]["values"] == [1, 2, 3]

        cls.ids.field_name = "changed_ids"

        query = cls({"ids": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0][
                   'ids'
               ]["values"] == [1, 2, 3]

    def test_logic_operator(self, cls):
        query = cls({"ids": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0][
                   'ids'
               ]["values"] == [1, 2, 3]

        cls.ids._logic_operator = "filter"

        query = cls({"ids": [1, 2, 3]}).query
        assert query['query']['bool']['filter'][0][
                   'ids'
               ]["values"] == [1, 2, 3]

        cls.ids._logic_operator = "should"

        query = cls({"ids": [1, 2, 3]}).query
        assert query['query']['bool']['should'][0][
                   'ids'
               ]["values"] == [1, 2, 3]


class TestCaseIdsElasticFieldIntegration:
    index_name = "test_ids"
    mappings = {
        "properties": {
            "sample": {
                "type": "text"
            },
        }
    }

    @pytest.mark.index_payload(name=index_name, mappings=mappings)
    @pytest.mark.parametrize("builder_params", [
        dict(
            parameter_name="ids_param",
            field=builder_fields.IdsElasticField(),
            value=[1, 2, 3],
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
