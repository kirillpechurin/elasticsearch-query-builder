from abc import ABC
from typing import Union, Optional, List, Tuple, Any


class FieldInterface:

    def get_query(self, value, field_name: str, **kwargs):
        raise NotImplementedError

    def normalize_input(self, value, field_query_name: str):
        raise NotImplementedError


class AbstractElasticField(FieldInterface):
    """
    Abstract Elasticsearch Field
    """
    _logic_operator = None

    def __init__(self,
                 logic_operator: Optional[str] = None,
                 field_name: Optional[str] = None):
        if logic_operator:
            self._logic_operator = logic_operator

        assert self._logic_operator is not None, "You must set logic operator"

        self._field_name = field_name

    @property
    def logic_operator(self):
        return self._logic_operator

    @property
    def field_name(self):
        return self._field_name

    @field_name.setter
    def field_name(self, value):
        self._field_name = value


class AdditionalQueryElasticFieldMixin:

    @staticmethod
    def _concatenate_query(default_query, additional_queries):
        logic_operator = "must"

        general_query = {"bool": {logic_operator: []}}
        for query in additional_queries:
            general_query["bool"][logic_operator].append(query)
        general_query["bool"][logic_operator].append(default_query)
        return general_query


class ConstructQueryElasticFieldMixin:

    @staticmethod
    def _construct(default: dict, attrs: List[Tuple[str, Any]]):
        for attr_name, attr_value in attrs:
            if attr_value is not None:
                default[attr_name] = attr_value
        return default


class ElasticField(AbstractElasticField,
                   AdditionalQueryElasticFieldMixin,
                   ConstructQueryElasticFieldMixin,
                   ABC):

    def get_query(self,
                  value,
                  field_name: str,
                  additional_queries: Optional[Union[list, dict]] = None):
        default_query = self._get_query(value, field_name)
        if additional_queries:
            return self._concatenate_query(
                default_query=default_query,
                additional_queries=additional_queries
            )
        return default_query

    def _get_query(self, value, field_name: str):
        raise NotImplementedError
