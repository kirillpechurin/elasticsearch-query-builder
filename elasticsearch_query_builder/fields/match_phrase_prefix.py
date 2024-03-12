from .abstract import ElasticField


class MatchPhrasePrefixElasticField(ElasticField):
    _logic_operator = "must"

    def _get_query(self, value, field_query_name: str):
        return {
            "match_phrase_prefix": {
                self._field_name: {
                    "query": value,
                }
            }
        }

    def normalize_input(self, value, field_query_name: str):
        return str(value)
