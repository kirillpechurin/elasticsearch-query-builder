from .abstract import ElasticField


class QueryStringElasticField(ElasticField):
    _logic_operator = "must"

    def __init__(self,
                 default_field: str = None,
                 fields: list = None,
                 fuzziness: str = None,
                 default_operator: str = None,
                 minimum_should_match: str = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        if default_field and len(fields):
            raise TypeError

        self._attrs = [
            ("fuzziness", fuzziness),
            ("default_operator", default_operator),
            ("minimum_should_match", minimum_should_match),
        ]
        if default_field:
            self._attrs.append(
                ("default_field", default_field)
            )
        elif fields:
            self._attrs.append(
                ("fields", fields)
            )
        else:
            self._attrs.append(
                ("default_field", self._field_name)
            )

    def _get_query(self, value, field_query_name):
        if not value:
            return {}

        return {
            "query_string": self._construct(
                default={
                    "query": value,
                },
                attrs=self._attrs
            )
        }

    def normalize_input(self, value, field_query_name: str):
        return str(value)
