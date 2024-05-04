import pytest

from elasticsearch_query_builder import fields as builder_fields
from .builder import ElasticSearchQueryTestBuilder


class TestCaseMultiMatchBestFieldsElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.multi_match_field = builder_fields.MultiMatchElasticField(
            query_type="best_fields",
            fields=[
                "sample",
                "test_field",
                "test_field_1",
            ]
        )
        return cls

    def test_query(self, cls):
        query = cls({"multi_match_field": "test-text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": "test-text",
                                "type": "best_fields",
                                "fields": [
                                    "sample",
                                    "test_field",
                                    "test_field_1",
                                ]
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"multi_match_field": "1"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "1"

        query = cls({"multi_match_field": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "[1, 2, 3]"

        query = cls({"multi_match_field": 3.0}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "3.0"

    def test_field_name(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field.field_name = "changed_multi_match_field"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "best_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ]
        }

    def test_logic_operator(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "filter"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['filter'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "should"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['should'][0]['multi_match']["query"] == "test-text"

    def test_default_attrs(self, cls):
        assert cls.multi_match_field._attrs == [
            ("operator", None),
            ("minimum_should_match", None),
            ("fuzziness", None),
            ("tie_breaker", None),
        ]

    def test_attr_operator(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", "AND"),
            ("minimum_should_match", None),
            ("fuzziness", None),
            ("tie_breaker", None),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "best_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "operator": "AND"
        }

    def test_attr_minimum_should_match(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", None),
            ("minimum_should_match", "85%"),
            ("fuzziness", None),
            ("tie_breaker", None),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "best_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "minimum_should_match": "85%"
        }

    def test_attr_fuzziness(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", None),
            ("minimum_should_match", None),
            ("fuzziness", "auto"),
            ("tie_breaker", None),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "best_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "fuzziness": "auto"
        }

    def test_attr_tie_breaker(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", None),
            ("minimum_should_match", None),
            ("fuzziness", None),
            ("tie_breaker", 1.54),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "best_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "tie_breaker": 1.54
        }

    def test_all_attrs(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", "AND"),
            ("minimum_should_match", "85%"),
            ("fuzziness", "auto"),
            ("tie_breaker", 1.54),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "best_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "operator": "AND",
            "minimum_should_match": "85%",
            "fuzziness": "auto",
            "tie_breaker": 1.54
        }


class TestCaseMultiMatchMostFieldsElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.multi_match_field = builder_fields.MultiMatchElasticField(
            query_type="most_fields",
            fields=[
                "sample",
                "test_field",
                "test_field_1",
            ]
        )
        return cls

    def test_query(self, cls):
        query = cls({"multi_match_field": "test-text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": "test-text",
                                "type": "most_fields",
                                "fields": [
                                    "sample",
                                    "test_field",
                                    "test_field_1",
                                ]
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"multi_match_field": "1"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "1"

        query = cls({"multi_match_field": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "[1, 2, 3]"

        query = cls({"multi_match_field": 3.0}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "3.0"

    def test_field_name(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field.field_name = "changed_multi_match_field"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "most_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ]
        }

    def test_logic_operator(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "filter"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['filter'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "should"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['should'][0]['multi_match']["query"] == "test-text"

    def test_default_attrs(self, cls):
        assert cls.multi_match_field._attrs == [
            ("operator", None),
            ("minimum_should_match", None),
            ("fuzziness", None),
        ]

    def test_attr_operator(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", "AND"),
            ("minimum_should_match", None),
            ("fuzziness", None),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "most_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "operator": "AND"
        }

    def test_attr_minimum_should_match(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", None),
            ("minimum_should_match", "85%"),
            ("fuzziness", None),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "most_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "minimum_should_match": "85%"
        }

    def test_attr_fuzziness(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", None),
            ("minimum_should_match", None),
            ("fuzziness", "auto"),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "most_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "fuzziness": "auto"
        }

    def test_all_attrs(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", "AND"),
            ("minimum_should_match", "85%"),
            ("fuzziness", "auto"),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "most_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "operator": "AND",
            "minimum_should_match": "85%",
            "fuzziness": "auto",
        }


class TestCaseMultiMatchPhraseElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.multi_match_field = builder_fields.MultiMatchElasticField(
            query_type="phrase",
            fields=[
                "sample",
                "test_field",
                "test_field_1",
            ]
        )
        return cls

    def test_query(self, cls):
        query = cls({"multi_match_field": "test-text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": "test-text",
                                "type": "phrase",
                                "fields": [
                                    "sample",
                                    "test_field",
                                    "test_field_1",
                                ]
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"multi_match_field": "1"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "1"

        query = cls({"multi_match_field": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "[1, 2, 3]"

        query = cls({"multi_match_field": 3.0}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "3.0"

    def test_field_name(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field.field_name = "changed_multi_match_field"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "phrase",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ]
        }

    def test_logic_operator(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "filter"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['filter'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "should"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['should'][0]['multi_match']["query"] == "test-text"

    def test_default_attrs(self, cls):
        assert cls.multi_match_field._attrs == []


class TestCaseMultiMatchPhrasePrefixElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.multi_match_field = builder_fields.MultiMatchElasticField(
            query_type="phrase_prefix",
            fields=[
                "sample",
                "test_field",
                "test_field_1",
            ]
        )
        return cls

    def test_query(self, cls):
        query = cls({"multi_match_field": "test-text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": "test-text",
                                "type": "phrase_prefix",
                                "fields": [
                                    "sample",
                                    "test_field",
                                    "test_field_1",
                                ]
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"multi_match_field": "1"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "1"

        query = cls({"multi_match_field": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "[1, 2, 3]"

        query = cls({"multi_match_field": 3.0}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "3.0"

    def test_field_name(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field.field_name = "changed_multi_match_field"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "phrase_prefix",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ]
        }

    def test_logic_operator(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "filter"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['filter'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "should"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['should'][0]['multi_match']["query"] == "test-text"

    def test_default_attrs(self, cls):
        assert cls.multi_match_field._attrs == []


class TestCaseMultiMatchCrossFieldsElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.multi_match_field = builder_fields.MultiMatchElasticField(
            query_type="cross_fields",
            fields=[
                "sample",
                "test_field",
                "test_field_1",
            ]
        )
        return cls

    def test_query(self, cls):
        query = cls({"multi_match_field": "test-text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": "test-text",
                                "type": "cross_fields",
                                "fields": [
                                    "sample",
                                    "test_field",
                                    "test_field_1",
                                ]
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"multi_match_field": "1"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "1"

        query = cls({"multi_match_field": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "[1, 2, 3]"

        query = cls({"multi_match_field": 3.0}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "3.0"

    def test_field_name(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field.field_name = "changed_multi_match_field"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "cross_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ]
        }

    def test_logic_operator(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "filter"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['filter'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "should"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['should'][0]['multi_match']["query"] == "test-text"

    def test_default_attrs(self, cls):
        assert cls.multi_match_field._attrs == [
            ("operator", None),
            ("minimum_should_match", None),
        ]

    def test_attr_operator(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", "AND"),
            ("minimum_should_match", None),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "cross_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "operator": "AND"
        }

    def test_attr_minimum_should_match(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", None),
            ("minimum_should_match", "85%"),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "cross_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "minimum_should_match": "85%"
        }

    def test_all_attrs(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", "AND"),
            ("minimum_should_match", "85%"),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "cross_fields",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "operator": "AND",
            "minimum_should_match": "85%",
        }


class TestCaseMultiMatchBoolPrefixElasticField:

    @pytest.fixture
    def cls(self):
        cls = ElasticSearchQueryTestBuilder
        cls.multi_match_field = builder_fields.MultiMatchElasticField(
            query_type="bool_prefix",
            fields=[
                "sample",
                "test_field",
                "test_field_1",
            ]
        )
        return cls

    def test_query(self, cls):
        query = cls({"multi_match_field": "test-text"}).query

        assert query == {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": "test-text",
                                "type": "bool_prefix",
                                "fields": [
                                    "sample",
                                    "test_field",
                                    "test_field_1",
                                ]
                            }
                        }
                    ]
                }
            }
        }

    def test_validation(self, cls):
        query = cls({"multi_match_field": "1"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "1"

        query = cls({"multi_match_field": [1, 2, 3]}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "[1, 2, 3]"

        query = cls({"multi_match_field": 3.0}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "3.0"

    def test_field_name(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field.field_name = "changed_multi_match_field"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "bool_prefix",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ]
        }

    def test_logic_operator(self, cls):
        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "filter"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['filter'][0]['multi_match']["query"] == "test-text"

        cls.multi_match_field._logic_operator = "should"

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['should'][0]['multi_match']["query"] == "test-text"

    def test_default_attrs(self, cls):
        assert cls.multi_match_field._attrs == [
            ("operator", None),
            ("minimum_should_match", None),
        ]

    def test_attr_operator(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", "AND"),
            ("minimum_should_match", None),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "bool_prefix",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "operator": "AND"
        }

    def test_attr_minimum_should_match(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", None),
            ("minimum_should_match", "85%"),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "bool_prefix",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "minimum_should_match": "85%"
        }

    def test_all_attrs(self, cls):
        cls.multi_match_field._attrs = [
            ("operator", "AND"),
            ("minimum_should_match", "85%"),
        ]

        query = cls({"multi_match_field": "test-text"}).query
        assert query['query']['bool']['must'][0]['multi_match'] == {
            "query": "test-text",
            "type": "bool_prefix",
            "fields": [
                "sample",
                "test_field",
                "test_field_1",
            ],
            "operator": "AND",
            "minimum_should_match": "85%",
        }


class TestCaseMultiMatchElasticFieldIntegration:
    index_name = "test_multi_match"
    mappings = {
        "properties": {
            "multi_match_text_1": {
                "type": "text"
            },
            "multi_match_text_2": {
                "type": "text"
            },
            "multi_match_text_3": {
                "type": "text"
            },
            "nested_multi_match": {
                "type": "nested",
                "properties": {
                    "multi_match_text_1": {
                        "type": "text"
                    },
                    "multi_match_text_2": {
                        "type": "text"
                    },
                    "multi_match_text_3": {
                        "type": "text"
                    },
                }
            }
        }
    }

    @pytest.mark.index_payload(name=index_name, mappings=mappings)
    @pytest.mark.parametrize("builder_params", [
        dict(
            parameter_name="multi_match_param",
            field=builder_fields.MultiMatchElasticField(
                query_type="best_fields",
                operator="AND",
                minimum_should_match="85%",
                fuzziness="auto",
                tie_breaker=0.3,
                fields=[
                    "multi_match_text_1",
                    "multi_match_text_2",
                    "multi_match_text_3",
                ]
            ),
            value="sample text",
        ),
        dict(
            parameter_name="multi_match_param",
            field=builder_fields.MultiMatchElasticField(
                query_type="most_fields",
                operator="AND",
                minimum_should_match="85%",
                fuzziness="auto",
                fields=[
                    "multi_match_text_1",
                    "multi_match_text_2",
                    "multi_match_text_3",
                ]
            ),
            value="sample text",
        ),
        dict(
            parameter_name="multi_match_param",
            field=builder_fields.MultiMatchElasticField(
                query_type="phrase",
                fields=[
                    "multi_match_text_1",
                    "multi_match_text_2",
                    "multi_match_text_3",
                ]
            ),
            value="sample text",
        ),
        dict(
            parameter_name="multi_match_param",
            field=builder_fields.MultiMatchElasticField(
                query_type="phrase_prefix",
                fields=[
                    "multi_match_text_1",
                    "multi_match_text_2",
                    "multi_match_text_3",
                ]
            ),
            value="sample text",
        ),
        dict(
            parameter_name="multi_match_param",
            field=builder_fields.MultiMatchElasticField(
                query_type="cross_fields",
                operator="AND",
                minimum_should_match="85%",
                fields=[
                    "multi_match_text_1",
                    "multi_match_text_2",
                    "multi_match_text_3",
                ]
            ),
            value="sample text",
        ),
        dict(
            parameter_name="multi_match_param",
            field=builder_fields.MultiMatchElasticField(
                query_type="bool_prefix",
                operator="AND",
                minimum_should_match="85%",
                fields=[
                    "multi_match_text_1",
                    "multi_match_text_2",
                    "multi_match_text_3",
                ]
            ),
            value="sample text",
        ),
        dict(
            parameter_name="nested_multi_match_param",
            field=builder_fields.NestedElasticField(
                path="nested_multi_match",
                child=builder_fields.MultiMatchElasticField(
                    query_type="best_fields",
                    operator="AND",
                    minimum_should_match="85%",
                    fuzziness="auto",
                    tie_breaker=0.3,
                    fields=[
                        "multi_match_text_1",
                        "multi_match_text_2",
                        "multi_match_text_3",
                    ]
                ),
            ),
            value="sample text",
        ),
    ])
    def test_request(self, elasticsearch_client, make_builder_instance, builder_params):
        query = make_builder_instance(builder_params).query
        data = elasticsearch_client.search(index=self.index_name, **query)
        assert isinstance(data, dict)
        assert data.get("hits") is not None
        assert data["hits"]["total"]["value"] == 0
