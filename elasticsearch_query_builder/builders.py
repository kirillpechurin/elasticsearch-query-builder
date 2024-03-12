from typing import Optional, Any, Dict

from elasticsearch_query_builder.fields.abstract import AbstractElasticField


class BaseQueryBuilder:

    def __init__(self,
                 params: Optional[dict] = None):
        params = self._processing_params(params)
        self._fields, self._params = self._assign_fields(params)

        self._query = None

    def _processing_params(self, params: Optional[dict]) -> dict:
        if params is None:
            return {}
        return params

    def _assign_fields(self, params: dict):
        fields = {}
        validated_params = {}

        for field_query_name, field_value in params.items():
            if not hasattr(self, field_query_name):
                # Field not found.
                continue

            field = getattr(self, field_query_name)
            self._assert_instance_field(field)

            fields[field_query_name] = getattr(self, field_query_name)
            validated_params[field_query_name] = field_value

        return (
            fields,
            validated_params
        )

    def _assert_instance_field(self, field: Any):
        raise NotImplementedError

    def _normalize_input(self, params: Dict[str, Any], fields: Dict[str, Any]):
        for field_query_name in params.keys():
            field = fields[field_query_name]
            try:
                params[field_query_name] = field.normalize_input(params[field_query_name], field_query_name)
            except ValueError:
                raise ValueError("Invalid input for `%s`" % field_query_name)

    @property
    def query(self):
        if self._query is None:
            self._normalize_input(self._params, self._fields)
            self._query = self._get_query()
        return self._query

    def _get_query(self):
        raise NotImplementedError


class ElasticsearchQueryBuilder(BaseQueryBuilder):
    _possible_logic_operators = (
        "must",
        "filter",
        "should",
        "must_not"
    )

    def _assert_instance_field(self, field: Any):
        assert isinstance(field, AbstractElasticField)

    def _get_additional_queries_by_field_name(self, field_name: str):
        func_name = "get_additional_%s_queries" % field_name
        if hasattr(self, func_name):
            return getattr(self, func_name)()
        return None

    def _get_query(self):
        query = {}

        for field_query_name, normalized_value in self._params.items():
            field = self._fields[field_query_name]

            additional_queries = self._get_additional_queries_by_field_name(field_query_name)
            field_query = field.get_query(
                normalized_value,
                field_query_name,
                additional_queries=additional_queries
            )
            if not field_query:
                continue

            if query.get(field.logic_operator) is None:
                assert field.logic_operator in self._possible_logic_operators
                query[field.logic_operator] = []

            if isinstance(field_query, list):
                query[field.logic_operator].extend(field_query)
            elif isinstance(field_query, dict):
                query[field.logic_operator].append(field_query)
            else:
                raise NotImplementedError

        return self._create_common_query(query)

    def _create_common_query(self, query):
        """
        Create common object query.
        """
        if not query:
            return {}
        return {
            "query": {
                "bool": {
                    key: value
                    for key, value in query.items()
                }
            }
        }
