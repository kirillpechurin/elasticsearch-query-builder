import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseMatchElasticFieldIntType:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.match_int = builder_fields.MatchElasticField(
            input_type=int,
            field_name="match_int_test",
        )
        return cls

    def test_query(self, cls):
        query = cls({"match_int": 1}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "match_int_test": {
                                    "query": 1
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"match_int": "1"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_int_test'
               ]["query"] == 1

        query = cls({"match_int": "3"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_int_test'
               ]["query"] == 3

        query = cls({"match_int": 3.0}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_int_test'
               ]["query"] == 3

    def test_field_name(self, cls):
        query = cls({"match_int": "1"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_int_test'
               ]["query"] == 1

        cls.match_int.field_name = "changed_match_int_test"

        query = cls({"match_int": "1"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'changed_match_int_test'
               ]["query"] == 1

    def test_logic_operator(self, cls):
        query = cls({"match_int": "1"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_int_test'
               ]["query"] == 1

        cls.match_int._logic_operator = "filter"

        query = cls({"match_int": "1"}).query
        assert query['query']['bool']['filter'][0]['match'][
                   'match_int_test'
               ]["query"] == 1

        cls.match_int._logic_operator = "should"

        query = cls({"match_int": "1"}).query
        assert query['query']['bool']['should'][0]['match'][
                   'match_int_test'
               ]["query"] == 1


class TestCaseMatchElasticFieldStringType:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.match_str = builder_fields.MatchElasticField(
            input_type=str,
            field_name="match_str_test"
        )
        return cls

    def test_query(self, cls):
        query = cls({"match_str": "test_text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "match_str_test": {
                                    "query": "test_text"
                                }
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"match_str": "test_text"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_str_test'
               ]["query"] == "test_text"

        query = cls({"match_str": "test"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_str_test'
               ]['query'] == "test"

        query = cls({"match_str": "test text"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_str_test'
               ]['query'] == 'test text'

    def test_field_name(self, cls):
        query = cls({"match_str": "test_text"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_str_test'
               ]["query"] == "test_text"

        cls.match_str.field_name = "changed_match_str_test"

        query = cls({"match_str": "test_text"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'changed_match_str_test'
               ]["query"] == "test_text"

    def test_logic_operator(self, cls):
        query = cls({"match_str": "test_text"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_str_test'
               ]["query"] == "test_text"

        cls.match_str._logic_operator = "filter"

        query = cls({"match_str": "test_text"}).query
        assert query['query']['bool']['filter'][0]['match'][
                   'match_str_test'
               ]["query"] == "test_text"

        cls.match_str._logic_operator = "should"

        query = cls({"match_str": "test_text"}).query
        assert query['query']['bool']['should'][0]['match'][
                   'match_str_test'
               ]["query"] == "test_text"

    def test_default_attrs(self, cls):
        assert cls.match_str._attrs == [
            ("operator", None),
            ("fuzziness", None),
            ("minimum_should_match", None),
        ]

    def test_attr_operator(self, cls):
        cls.match_str._attrs = [
            ("operator", "AND"),
            ("fuzziness", None),
            ("minimum_should_match", None),
        ]

        query = cls({"match_str": "test_text"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_str_test'
               ] == {
                   "query": "test_text",
                   "operator": "AND"
               }

    def test_attr_fuzziness(self, cls):
        cls.match_str._attrs = [
            ("operator", None),
            ("fuzziness", "auto"),
            ("minimum_should_match", None),
        ]

        query = cls({"match_str": "test_text"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_str_test'
               ] == {
                   "query": "test_text",
                   "fuzziness": "auto"
               }

    def test_attr_minimum_should_match(self, cls):
        cls.match_str._attrs = [
            ("operator", None),
            ("fuzziness", None),
            ("minimum_should_match", "85%"),
        ]

        query = cls({"match_str": "test_text"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_str_test'
               ] == {
                   "query": "test_text",
                   "minimum_should_match": "85%"
               }

    def test_all_attrs(self, cls):
        cls.match_str._attrs = [
            ("operator", "AND"),
            ("fuzziness", "auto"),
            ("minimum_should_match", "85%"),
        ]

        query = cls({"match_str": "test_text"}).query
        assert query['query']['bool']['must'][0]['match'][
                   'match_str_test'
               ] == {
                   "query": "test_text",
                   "operator": "AND",
                   "fuzziness": "auto",
                   "minimum_should_match": "85%"
               }


class TestCaseMatchElasticFieldIntegration:
    index_name = "test_match"
    mappings = {
        "properties": {
            "match_int": {
                "type": "integer"
            },
            "match_text": {
                "type": "text"
            },
            "nested_match": {
                "type": "nested",
                "properties": {
                    "match_int": {
                        "type": "integer"
                    },
                    "match_text": {
                        "type": "text"
                    }
                }
            }
        }
    }

    @pytest.mark.index_payload(name=index_name, mappings=mappings)
    @pytest.mark.parametrize("builder_params", [
        dict(
            parameter_name="match_int_param",
            field=builder_fields.MatchElasticField(
                field_name="match_int",
                input_type=int
            ),
            value=1,
        ),
        dict(
            parameter_name="choice_text_param",
            field=builder_fields.MatchElasticField(
                field_name="match_text",
                input_type=str,
                operator="AND",
                fuzziness="auto",
                minimum_should_match="85%"
            ),
            value="sample text",
        ),
        dict(
            parameter_name="nested_match_int_param",
            field=builder_fields.NestedElasticField(
                path="nested_match",
                child=builder_fields.MatchElasticField(
                    field_name="match_int",
                    input_type=int
                ),
            ),
            value=3,
        ),
        dict(
            parameter_name="nested_match_text_param",
            field=builder_fields.NestedElasticField(
                path="nested_match",
                child=builder_fields.MatchElasticField(
                    field_name="match_text",
                    input_type=str,
                    operator="AND",
                    fuzziness="auto",
                    minimum_should_match="85%"
                ),
            ),
            value="sample text",
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
