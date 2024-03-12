from typing import Optional

from .abstract import ElasticField


class ExistsElasticField(ElasticField):
    _logic_operator = "must"

    def _get_query(self, value: Optional[bool], field_name: str):
        if value is None:
            return {}
        elif value is True:
            self._logic_operator = "must"
        elif value is False:
            self._logic_operator = "must_not"

        return {
            "exists": {
                "field": self._field_name
            }
        }

    def normalize_input(self, value, field_query_name: str):
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value == 'true'
        else:
            raise ValueError
