from .abstract import ElasticField


class MatchPhraseElasticField(ElasticField):
    _logic_operator = "must"

    def _get_query(self, value, field_query_name: str):
        return {
            "match_phrase": {
                self._field_name: {
                    "query": value,
                }
            }
        }

    def normalize_input(self, value, field_query_name: str):
        return str(value)
