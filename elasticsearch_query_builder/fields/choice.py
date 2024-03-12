from typing import Union

from .abstract import ElasticField


class ChoiceElasticField(ElasticField):
    _logic_operator = "must"

    def __init__(self,
                 choices: list,
                 child: ElasticField,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self._choices = choices
        self._child = child

    def get_query(self, value, field_name: str, additional_queries: Union[list, dict, None] = None):
        if value not in self._choices:
            return {}

        return self._child.get_query(value, field_name, additional_queries)

    def normalize_input(self, value, field_name: str):
        return self._child.normalize_input(value, field_name)
