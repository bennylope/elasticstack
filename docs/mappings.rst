==========================
Configurable index mapping
==========================

ElasticSearch gives you fine grained control over how your indexed content is
analyzed, from choosing between `built-in analyzers
<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/analysis-analyzers.html>`_,
choosing options for built-in analyzers, and creating your own from existing
tokenizers and filters.

.. note::
    An analyzer is a combination of a tokenizer and one or more text filters.
    The tokenizer is responsible for breaking apart the text into individual
    "tokens", which could be words or pieces of words. The filters are
    responsible for transforming and removing tokens from the indexed content,
    e.g. making all text lowercase, removing common words, indexing synonyms,
    etc.

The default ElasticSearch backend in Haystack doesn't expose any of this
configuration however. The search mapping provided by this backend maps
non-nGram text fields to the `snowball analyzer
<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/analysis-snowball-analyzer.html>`_.
This is a pretty good default for English, but may not meet your requirements
and won't work well for non-English languages.

The elasticstack backend takes advantage of the Haystack backend's structure to
make it relatively simple to override and extend the search mapping in your
project.

elasticstack lets you manage your index mapping in three ways:

1. Changing the default analyzer
2. Specifying an analyzer for an individual `SearchIndex` field
3. Specifying a complete search mapping including custom analyzers

Haystack configuration
======================

First, you'll need to ensure that you're using the elasticstack backend, not
Haystack's. Your `HAYSTACK_CONNECTIONS` should look something like this, so
that the `ENGINE` value for any defined search index is using the elasticstack
search engine class.::

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'elasticstack.backends.ConfigurableElasticSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }

And of course make sure you've followed the instructions for `installing
Haystack <http://django-haystack.readthedocs.org/en/latest/tutorial.html>`_ and
your ElasticSearch instance.

.. important::
    All of the options described here depend on this configurable search engine
    backend.


Chaning the default analyzer
============================

Haystack will map the `snowball` analyzer to non-nGram text content by default.

You can specify an alternate analyzer using the
`ELASTICSEARCH_DEFAULT_ANALYZER` setting in your `settings.py` file::

    ELASTICSEARCH_DEFAULT_ANALYZER = 'stop'

Any field that would have been analyzed with the `snowball` analyzer will now
use the `stop
<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/analysis-stop-analyzer.html>`_
analyzer.


Choosing a field-specific analyzer
==================================

Even with a new default analyzer you may want to change this on a field by
field basis as fits your needs. To do so, use the fields from
`elasticstack.fields` to specify your analyzer with the `analyzer` keyword
argument::

    from haystack import indexes
    from haystack.fields import CharField as BaseCharField
    from elasticstack.fields import CharField
    from myapp.models import MyContent

    class MyContentIndex(indexes.SearchIndex, indexes.Indexable):
        text = CharField(document=True, use_template=True,
                analyzer='stop')
        body = BaseCharField(use_template=True)

        def get_model(self):
            return MyContent

Now the `text` field will be indexed using the `stop` analyzer, and the `body`
field will be indexed using the default analyzer.

.. attention::

    Using a configurable field without specifying an analyzer will raise a
    `ValueError`.


Custom analyzers and additional configuration
=============================================

If instead you need to configure an analyzer, define your own, or in any way
further customize the search mapping, you can customize the base `analysis
settings
<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/analysis.html>`_
for your index.

You do this by creating a dictionary of analysis settings in your `settings.py`
file for the `ELASTICSEARCH_INDEX_SETTINGS` setting.

This example takes the default mapping and adds a synonym analyzer.

.. code-block:: python
   :linenos:

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

The two additions to this mapping are the `synonym_analyzer` at line 5 and the
`synonym` filter at line 45.

Adding this mapping in and of itself does nothing more than make your new
analyzer available. To use it you either need to change your
`ELASTICSEARCH_DEFAULT_ANALYZER` or specify the analyzer in the search index field.

Realizing custom changes
========================

Even with all of these changes you won't notice any difference in your queries
until you've reindexed your content. The mappings for your search index define
how that content is handled when it goes into the index; it does nothing for
content already there.
