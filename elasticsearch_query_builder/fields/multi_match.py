from .abstract import ElasticField


class MultiMatchElasticField(ElasticField):
    _logic_operator = "must"

    def __init__(self,
                 query_type: str,
                 fields: list,
                 operator: str = None,
                 minimum_should_match: str = None,
                 tie_breaker: float = None,
                 fuzziness: str = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._query_type = query_type
        self._fields = fields
        self._operator = operator
        self._minimum_should_match = minimum_should_match
        self._tie_breaker = tie_breaker
        self._fuzziness = fuzziness
        self._attrs = self._get_attrs_by_query_type(query_type)

    def _get_attrs_by_query_type(self, query_type: str):
        if query_type == "best_fields":
            return [
                ("operator", self._operator),
                ("minimum_should_match", self._minimum_should_match),
                ("fuzziness", self._fuzziness),
                ("tie_breaker", self._tie_breaker),
            ]
        elif query_type == "most_fields":
            return [
                ("operator", self._operator),
                ("minimum_should_match", self._minimum_should_match),
                ("fuzziness", self._fuzziness),
            ]
        elif query_type == "phrase":
            return []
        elif query_type == "phrase_prefix":
            return []
        elif query_type == "cross_fields":
            return [
                ("operator", self._operator),
                ("minimum_should_match", self._minimum_should_match),
            ]
        elif query_type == "bool_prefix":
            return [
                ("operator", self._operator),
                ("minimum_should_match", self._minimum_should_match),
            ]
        else:
            raise TypeError("Unknown query type: %s" % query_type)

    def _get_query(self, value, field_query_name: str):
        query = self._construct(
            default={
                "query": value,
                "type": self._query_type,
                "fields": self._fields
            },
            attrs=self._attrs
        )
        return {
            "multi_match": query
        }

    def normalize_input(self, value, field_query_name: str):
        return str(value)
