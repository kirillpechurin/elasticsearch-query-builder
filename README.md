# Elasticsearch Query Builder  

[![CI](https://github.com/kirillpechurin/elasticsearch-query-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/kirillpechurin/elasticsearch-query-builder/actions/workflows/ci.yml)

[![codecov](https://codecov.io/github/kirillpechurin/elasticsearch-query-builder/graph/badge.svg?token=U9BZNOTV72)](https://codecov.io/github/kirillpechurin/elasticsearch-query-builder)

[![pypi](https://badge.fury.io/py/elasticsearch-query-builder.svg)](https://pypi.python.org/pypi/elasticsearch-query-builder)

---
#### A tool for forming a single query body for further search in Elasticsearch

## Features
* A single entry point for receiving a ready-made request
* Support for the most frequently used fields
* Basic normalization of input data with the ability to specify the type
* No dependencies

## Installation

Requirements:
- Installed python `3.8` or higher

```shell
pip install elasticsearch-query-builder
```

## Usage
To use Elasticsearch query builder, you need to describe the inheritor class from the base builder class, and then describe the expected fields as class attributes

```python
from elasticsearch_query_builder import ElasticsearchQueryBuilder, fields


class BookQueryBuilder(ElasticsearchQueryBuilder):
    search = fields.MultiMatchElasticField(
        query_type="best_fields",
        fields=[
            "field_1",
            "field_2",
            "field_3",
            "obj.field_4",
        ]
    )

    with_reviews = fields.TermElasticField(
        input_type=bool,
        field_name="has_reviews"
    )

    author = fields.NestedElasticField(
        path="authors",
        child=fields.MatchElasticField(
            input_type=str,
            field_name="name"
        )
    )
```

The next step is to call the described class, passing it an object with request parameters in the constructor

```
...

builder = BookQueryBuilder({"search": "World", "with_reviews": "true", "author": "John Doe"})
query = builder.query
print(query)
```

As a result of execution, a query object will be constructed, which can be sent to Elasticsearch for search
```json
{
    "query": {
        "bool": {
            "must": [
                {
                    "multi_match": {
                        "query": "World",
                        "type": "best_fields",
                        "fields": [
                            "field_1",
                            "field_2",
                            "field_3",
                            "obj.field_4"
                        ]
                    }
                },
                {
                    "term": {
                        "has_reviews": true
                    }
                },
                {
                    "nested": {
                        "path": "authors",
                        "query": {
                            "match": {
                                "authors.name": {
                                    "query": "John Doe"
                                }
                            }
                        }
                    }
                }
            ]
        }
    }
}
```
