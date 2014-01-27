===================
Management commands
===================

The extra management commands are small tools to help in diagnosing problems
with unexpected search results, by showing you how your data is actually mapped
for ElasticSearch and how a specific model instance (with a matching
`SearchIndex` class) is mapped as an example.

show_mapping
============

Make a change and wonder why your results don't look as expected? The
management command `show_mapping` will print the current mapping for
your defined search index(es). At the least it may show that you've simply
forgotten to update your index with new mappings::

    python manage.py show_mapping

By default this will display the `existing_mapping` which shows the index,
document type, and document properties.::

    {
        "haystack": {
            "modelresult": {
                "properties": {
                    "is_active": {
                        "type": "boolean"
                    },
                    "text": {
                        "type": "string"
                    },
                    "published": {
                        "type": "date",
                        "format": "dateOptionalTime"
                    }
                }
            }
        }
    }

If you provide the `--detail` flag this will return only the field mappings but
including additional details, such as boost levels and field-specific
analyzers.::

    {
        "is_active": {
            "index": "not_analyzed",
            "boost": 1,
            "store": "yes",
            "type": "boolean"
        },
        "text": {
            "index": "analyzed",
            "term_vector": "with_positions_offsets",
            "type": "string",
            "analyzer": "custom_analyzer",
            "boost": 1,
            "store": "yes"
        },
        "pub_date": {
            "index": "analyzed",
            "boost": 1,
            "store": "yes",
            "type": "date"
        }
    }

show_document
=============

Provided the name of an indexed model and a key it generates and prints the
generated document for this object::

    python manage.py show_document myapp.MyModel 19181

The JSON document will be formatted with 'pretty' indenting.
