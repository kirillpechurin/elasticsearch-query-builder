from .abstract import ElasticField


class RangeElasticField(ElasticField):
    _logic_operator = "must"

    def __init__(self,
                 input_type: type,
                 lookup_expr: str,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        assert lookup_expr in ("gte", "lte", "gt", "lt")
        self._lookup_expr = lookup_expr
        self._input_type = input_type

    def _get_query(self, value, field_query_name: str):
        if not value:
            return {}

        return {
            "range": {
                self._field_name: {
                    self._lookup_expr: value,
                }
            }
        }

    def normalize_input(self, value, field_name: str):
        if self._input_type == float:
            return float(value)
        elif self._input_type == int:
            return int(value)
        else:
            raise ValueError
