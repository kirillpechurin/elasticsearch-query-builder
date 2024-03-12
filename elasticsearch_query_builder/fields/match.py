from .abstract import ElasticField


class MatchElasticField(ElasticField):
    _logic_operator = "must"

    def __init__(self,
                 input_type: type,
                 operator: str = None,
                 fuzziness: str = None,
                 minimum_should_match: str = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._input_type = input_type
        self._attrs = [
            ("operator", operator),
            ("fuzziness", fuzziness),
            ("minimum_should_match", minimum_should_match),
        ]

    def _get_query(self, value, field_name: str):
        if not value:
            return {}

        return {
            "match": {
                self._field_name: self._construct(
                    default={
                        "query": value,
                    },
                    attrs=self._attrs
                )
            }
        }

    def normalize_input(self, value, field_name: str):
        if self._input_type == int:
            return int(value)
        elif self._input_type == str:
            return str(value)
        else:
            raise ValueError
