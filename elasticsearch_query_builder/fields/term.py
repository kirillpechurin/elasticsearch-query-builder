from typing import Union

from .abstract import ElasticField


class TermElasticField(ElasticField):
    _logic_operator = "must"

    def __init__(self,
                 input_type: type,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._input_type = input_type

    def _get_query(self, value, field_query_name: str, additional_queries: Union[list, dict, None] = None):
        return {
            "term": {
                self._field_name:  value
            }
        }

    def normalize_input(self, value, field_query_name: str):
        if self._input_type == bool:
            if isinstance(value, str):
                return value == "true"
            elif isinstance(value, bool):
                return value
            else:
                raise ValueError
        elif self._input_type == str:
            return str(value)
        elif self._input_type == int:
            return int(value)
        else:
            raise ValueError
