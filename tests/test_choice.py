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
        assert query['query']['bool']['must'][0]['match']['choice_test']["query"] == 1

        query = cls({"choice": 1}).query
        assert query['query']['bool']['must'][0]['match']['choice_test']["query"] == 1

        cls.choice._child._input_type = str
        query = cls({"choice": "1"}).query
        assert query == {}

        cls.choice._choices = ["1", "2", "3"]
        query = cls({"choice": "1"}).query
        assert query['query']['bool']['must'][0]['match']['choice_test']["query"] == "1"

    def test_field_name(self, cls):
        query = cls({"choice": 1}).query
        assert query['query']['bool']['must'][0]['match']['choice_test']["query"] == 1

        cls.choice._child.field_name = "changed_choice_test"

        query = cls({"choice": 1}).query
        assert query['query']['bool']['must'][0]['match']['changed_choice_test']["query"] == 1

    def test_choices(self, cls):
        for i in range(1, 3 + 1):
            query = cls({"choice": i}).query
            assert query['query']['bool']['must'][0]['match']['choice_test']["query"] == i
            query = cls({"choice": str(i)}).query
            assert query['query']['bool']['must'][0]['match']['choice_test']["query"] == i

        cls.choice._choices = ['1', '2', '3']
        cls.choice._child._input_type = str

        for i in range(1, 3 + 1):
            query = cls({"choice": i}).query
            assert query['query']['bool']['must'][0]['match']['choice_test']['query'] == str(i)
            query = cls({"choice": str(i)}).query
            assert query['query']['bool']['must'][0]['match']['choice_test']['query'] == str(i)

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
        assert query['query']['bool']['must'][0]['match']['choice_test']['query'] == "1"

        query = cls({"choice": 1}).query
        assert query['query']['bool']['must'][0]['match']['choice_test']['query'] == "1"

        cls.choice._child._input_type = int
        query = cls({"choice": "1"}).query
        assert query == {}

        cls.choice._choices = [1, 2, 3]
        query = cls({"choice": "1"}).query
        assert query['query']['bool']['must'][0]['match']['choice_test']["query"] == 1

    def test_field_name(self, cls):
        query = cls({"choice": "1"}).query
        assert query['query']['bool']['must'][0]['match']['choice_test']['query'] == "1"

        cls.choice._child.field_name = "changed_choice_test"

        query = cls({"choice": "1"}).query
        assert query['query']['bool']['must'][0]['match']['changed_choice_test']['query'] == "1"

    def test_choices(self, cls):
        for i in range(1, 3 + 1):
            query = cls({"choice": i}).query
            assert query['query']['bool']['must'][0]['match']['choice_test']['query'] == str(i)
            query = cls({"choice": str(i)}).query
            assert query['query']['bool']['must'][0]['match']['choice_test']['query'] == str(i)

        query = cls({"choice": "6"}).query
        assert query == {}
