import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseChoiceElasticFieldIntType:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.choice = builder_fields.ChoiceElasticField(
            choices=[1, 2, 3],
            child=builder_fields.MatchElasticField(
                field_name="choice_test",
                input_type=int
            )
        )
        return cls

    def test_query(self, cls):
        query = cls({"choice": 1}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "choice_test": {
                                    "query": 1
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_child_validation(self, cls):
        query = cls({"choice": "1"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'choice_test'
               ]["query"] == 1

        query = cls({"choice": 1}).query
        assert query['query']['bool']['must'][0]['match'][
                   'choice_test'
               ]["query"] == 1

        cls.choice._child._input_type = str
        query = cls({"choice": "1"}).query
        assert query == {}

        cls.choice._choices = ["1", "2", "3"]
        query = cls({"choice": "1"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'choice_test'
               ]["query"] == "1"

    def test_field_name(self, cls):
        query = cls({"choice": 1}).query
        assert query['query']['bool']['must'][0]['match'][
                   'choice_test'
               ]["query"] == 1

        cls.choice._child.field_name = "changed_choice_test"

        query = cls({"choice": 1}).query
        assert query['query']['bool']['must'][0]['match'][
                   'changed_choice_test'
               ]["query"] == 1

    def test_choices(self, cls):
        for i in range(1, 3 + 1):
            query = cls({"choice": i}).query
            assert query['query']['bool']['must'][0]['match'][
                       'choice_test'
                   ]["query"] == i
            query = cls({"choice": str(i)}).query
            assert query['query']['bool']['must'][0]['match'][
                       'choice_test'
                   ]["query"] == i

        cls.choice._choices = ['1', '2', '3']
        cls.choice._child._input_type = str

        for i in range(1, 3 + 1):
            query = cls({"choice": i}).query
            assert query['query']['bool']['must'][0]['match'][
                       'choice_test'
                   ]['query'] == str(i)
            query = cls({"choice": str(i)}).query
            assert query['query']['bool']['must'][0]['match'][
                       'choice_test'
                   ]['query'] == str(i)

        query = cls({"choice": 6}).query
        assert query == {}


class TestCaseChoiceElasticFieldStringType:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.choice = builder_fields.ChoiceElasticField(
            choices=["1", "2", "3"],
            child=builder_fields.MatchElasticField(
                field_name="choice_test",
                input_type=str
            )
        )
        return cls

    def test_query(self, cls):
        query = cls({"choice": "1"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "choice_test": {
                                    "query": "1"
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_child_validation(self, cls):
        query = cls({"choice": "1"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'choice_test'
               ]['query'] == "1"

        query = cls({"choice": 1}).query
        assert query['query']['bool']['must'][0]['match'][
                   'choice_test'
               ]['query'] == "1"

        cls.choice._child._input_type = int
        query = cls({"choice": "1"}).query
        assert query == {}

        cls.choice._choices = [1, 2, 3]
        query = cls({"choice": "1"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'choice_test'
               ]["query"] == 1

    def test_field_name(self, cls):
        query = cls({"choice": "1"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'choice_test'
               ]['query'] == "1"

        cls.choice._child.field_name = "changed_choice_test"

        query = cls({"choice": "1"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'changed_choice_test'
               ]['query'] == "1"

    def test_choices(self, cls):
        for i in range(1, 3 + 1):
            query = cls({"choice": i}).query
            assert query['query']['bool']['must'][0]['match'][
                       'choice_test'
                   ]['query'] == str(i)
            query = cls({"choice": str(i)}).query
            assert query['query']['bool']['must'][0]['match'][
                       'choice_test'
                   ]['query'] == str(i)

        query = cls({"choice": "6"}).query
        assert query == {}


class TestCaseChoiceElasticFieldIntegration:
    index_name = "test_choice"
    mappings = {
        "properties": {
            "choice_int": {
                "type": "integer"
            },
            "choice_text": {
                "type": "text"
            },
            "nested_choice": {
                "type": "nested",
                "properties": {
                    "choice_int": {
                        "type": "integer"
                    },
                    "choice_text": {
                        "type": "text"
                    }
                }
            }
        }
    }

    @pytest.mark.index_payload(name=index_name, mappings=mappings)
    @pytest.mark.parametrize("builder_params", [
        dict(
            parameter_name="choice_int_param",
            field=builder_fields.ChoiceElasticField(
                choices=[1, 2, 3],
                child=builder_fields.MatchElasticField(
                    field_name="choice_int",
                    input_type=int
                )
            ),
            value=1,
        ),
        dict(
            parameter_name="choice_text_param",
            field=builder_fields.ChoiceElasticField(
                choices=["1", "2", "3"],
                child=builder_fields.MatchElasticField(
                    field_name="choice_text",
                    input_type=str
                )
            ),
            value="1",
        ),
        dict(
            parameter_name="nested_choice_int_param",
            field=builder_fields.NestedElasticField(
                path="nested_choice",
                child=builder_fields.ChoiceElasticField(
                    choices=[1, 2, 3],
                    child=builder_fields.MatchElasticField(
                        field_name="choice_int",
                        input_type=int
                    )
                )
            ),
            value=3,
        ),
        dict(
            parameter_name="nested_choice_text_param",
            field=builder_fields.NestedElasticField(
                path="nested_choice",
                child=builder_fields.ChoiceElasticField(
                    choices=["1", "2", "3"],
                    child=builder_fields.MatchElasticField(
                        field_name="choice_text",
                        input_type=str
                    )
                )
            ),
            value="3",
        )
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
