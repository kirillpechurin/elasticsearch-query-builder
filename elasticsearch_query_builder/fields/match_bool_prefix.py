from .abstract import ElasticField


class MatchBoolPrefixElasticField(ElasticField):
    _logic_operator = "must"

    def __init__(self,
                 operator: str = None,
                 minimum_should_match: str = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._attrs = [
            ("operator", operator),
            ("minimum_should_match", minimum_should_match),
        ]

    def _get_query(self, value, field_name: str):
        if not value:
            return {}

        return {
            "match_bool_prefix": {
                self._field_name: self._construct(
                    default={
                        "query": value,
                    },
                    attrs=self._attrs
                )
            }
        }

    def normalize_input(self, value, field_query_name: str):
        return str(value)
