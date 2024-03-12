from typing import Union

from .abstract import ElasticField


class NestedElasticField(ElasticField):
    _logic_operator = "must"

    def __init__(self,
                 path: str,
                 child: ElasticField,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._path = path
        self._child = child

    def get_query(self,
                  value,
                  field_name: str,
                  additional_queries: Union[list, dict, None] = None):
        if not additional_queries:
            additional_queries = {}
        nested_additional_queries = additional_queries.pop(self._path, None)

        # Get default child field name.
        default_child_field_name = self._child.field_name
        # Set normalized child field name with nested path.
        self._child.field_name = f"{self._path}.{default_child_field_name}"
        # Get query for child.
        query = self._child.get_query(value, field_name, additional_queries=additional_queries)
        # Reset child field name.
        self._child.field_name = default_child_field_name

        if not query:
            return {}

        default_query = {
            "nested": {
                "path": self._path,
                "query": query
            }
        }
        if nested_additional_queries:
            default_query['nested']['query'] = self._concatenate_query(
                default_query=default_query['nested']['query'],
                additional_queries=nested_additional_queries
            )
        return default_query

    def normalize_input(self, value, field_name: str):
        return self._child.normalize_input(value, field_name)
