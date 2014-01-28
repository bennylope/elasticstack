==========================
Configurable index mapping
==========================

The search mapping provided by Haystack's ElasticSearch backend includes brief
but sensible defaults for nGram analysis.

Default analyzer
================

ElasticSearch will use an `analyzer
<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/analysis-analyzers.html>`_
to index your searchable content. By default Haystack will specify that the
`snowball analyzer
<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/analysis-snowball-analyzer.html>`_
be used for all searchable content.

You can specify an alternate analyzer using the
`ELASTICSEARCH_DEFAULT_ANALYZER` setting in your settings.py file::

    ELASTICSEARCH_DEFAULT_ANALYZER = 'stop'

Any field that would have been analyzed with the `snowball` analyzer will now
use the `stop
<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/analysis-stop-analyzer.html>`_
analyzer.

Custom analyzers and additional configuration
=============================================

You can add change these settings or add your own mappings by providing a
mapping dictionary using
`ELASTICSEARCH_INDEX_SETTINGS` in your settings file. This example takes the
default mapping and adds a synonym analyzer::

    ELASTICSEARCH_INDEX_SETTINGS = {
        'settings': {
            "analysis": {
                "analyzer": {
                    "synonym_analyzer" : {
                        "type": "custom",
                        "tokenizer" : "standard",
                        "filter" : ["synonym"]
                    },
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "lowercase",
                        "filter": ["haystack_ngram", "synonym"]
                    },
                    "edgengram_analyzer": {
                        "type": "custom",
                        "tokenizer": "lowercase",
                        "filter": ["haystack_edgengram"]
                    }
                },
                "tokenizer": {
                    "haystack_ngram_tokenizer": {
                        "type": "nGram",
                        "min_gram": 3,
                        "max_gram": 15,
                    },
                    "haystack_edgengram_tokenizer": {
                        "type": "edgeNGram",
                        "min_gram": 2,
                        "max_gram": 15,
                        "side": "front"
                    }
                },
                "filter": {
                    "haystack_ngram": {
                        "type": "nGram",
                        "min_gram": 3,
                        "max_gram": 15
                    },
                    "haystack_edgengram": {
                        "type": "edgeNGram",
                        "min_gram": 2,
                        "max_gram": 15
                    },
                    "synonym" : {
                        "type" : "synonym",
                        "ignore_case": "true",
                        "synonyms_path" : "synonyms.txt"
                    }
                }
            }
        }
    }

The synonym filter is ready for your index, but will go unused yet. Changing
the default analyzer will now enable this analyzer as the default::

    ELASTICSEARCH_DEFAULT_ANALYZER = 'synonym_analyzer'

Now all your analyzed fields, except for nGram fields, will be analyzed using
`synonym_analyzer`.

Field based analyzers
=====================

Even with a new default analyzer you may want to change this on a field by
field basis as fits your needs. To do so, use the fields from
`elasticstack.fields` to specify your analyzer with the `analyzer` keyword
argument::

    from haystack import indexes
    from elasticstack.fields import CharField
    from myapp.models import MyContent

    class MyContentIndex(indexes.SearchIndex, indexes.Indexable):
        text = CharField(document=True, use_template=True,
                analyzer='synonym_analyzer')

        def get_model(self):
            return MyContent

