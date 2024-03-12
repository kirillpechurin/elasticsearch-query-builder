from collections import abc
from typing import Optional

from .abstract import ElasticField


class IdsElasticField(ElasticField):
    _logic_operator = "must"

    def _get_query(self, value: Optional[list], field_name: str):
        if not value:
            return {}

        return {
            "ids": {
                "values": value
            }
        }

    def normalize_input(self, value, field_query_name: str):
        if isinstance(value, abc.Iterable):
            return list(value)
        else:
            raise ValueError
