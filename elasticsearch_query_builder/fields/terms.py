from collections import abc

from .abstract import ElasticField


class TermsElasticField(ElasticField):
    _logic_operator = "must"

    def _get_query(self, value, field_query_name):
        if not value:
            return {}
        return {
            "terms": {
                self._field_name: value
            }
        }

    def normalize_input(self, value, field_query_name):
        if isinstance(value, abc.Iterable):
            return list(value)
        else:
            raise ValueError
