============
elasticstack
============

.. image:: https://badge.fury.io/py/elasticstack.svg
    :target: http://badge.fury.io/py/elasticstack

.. image:: https://travis-ci.org/bennylope/elasticstack.svg?branch=master
        :target: https://travis-ci.org/bennylope/elasticstack

.. image:: https://pypip.in/d/elasticstack/badge.svg
        :target: https://crate.io/packages/elasticstack?version=latest

:Version: 0.4.1
:Author: Ben Lopatin (http://benlopatin.com)

Configurable indexing and other extras for Haystack (with ElasticSearch
biases).

Full documentation is on `Read the Docs <http://elasticstack.readthedocs.org/en/latest/>`_.

Requirements
============

* `Django <https://www.djangoproject.com/>`_: tested against Django 1.8, and 1.9
* `Haystack <http://www.haystacksearch.org/>`_: tested against Haystack 2.4.0,
  it should work with any combination of Haystack and Django that work
* `ElasticSearch <http://www.elasticsearch.org/>`_: presumably any newish
  version will do, however the only version tested against so far is 0.19.x

Features and goals
==================

Some of these features are backend agnostic but most features have
ElasticSearch in mind.

For more background see the blog post `Stretching Haystack's ElasticSearch Backend <http://www.wellfireinteractive.com/blog/custom-haystack-elasticsearch-backend/>`_.

Global configurable index mapping
---------------------------------

The search mapping provided by Haystack's ElasticSearch backend includes brief
but sensible defaults for nGram analysis. You can globaly add change these settings or
add your own mappings by providing a mapping dictionary using
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

The synonym filter is ready for your index, but will go unused yet. 

Before your new analyzer can be used you will need to change your Haystack engine and rebuild/update
your index. In your `settings.py` modify `HAYSTACK_CONNECTIONS` accordingly::

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'elasticstack.backends.ConfigurableElasticSearchEngine',
            'URL': env_var('HAYSTACK_URL', 'http://127.0.0.1:9200/'),
            'INDEX_NAME': 'haystack',
        },
    }

The default analyzer for non-nGram fields in Haystack's ElasticSearch backend
is the `snowball analyzer <http://www.elasticsearch.org/guide/reference/index-modules/analysis/snowball-analyzer.html>`_.
A perfectly good analyzer but not necessarily what you need. It's also language
specific (English by default).

Specify your analyzer with `ELASTICSEARCH_DEFAULT_ANALYZER` in your settings
file::

    ELASTICSEARCH_DEFAULT_ANALYZER = 'synonym_analyzer'

Now all your analyzed fields, except for nGram fields, will be analyzed using
`synonym_analyzer`.

If you want to specify a custom search_analyzer for nGram/EdgeNgram fields,
define it with the `ELASTICSEARCH_DEFAULT_NGRAM_SEARCH_ANALYZER` settings::

    ELASTICSEARCH_DEFAULT_NGRAM_SEARCH_ANALYZER = 'standard'

Configurable index mapping per index
------------------------------------

Alternatively you can configure index mapping per index. This is usefull for multilanguage index settup.
In this case `HAYSTACK_CONNECTION` contains key `SETTINGS_NAME` have to match with name in `ELASTICSEARCH_INDEX_SETTINGS`::


    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'elasticstack.backends.ConfigurableElasticSearchEngine',
            'URL': env_var('HAYSTACK_URL', 'http://127.0.0.1:9200/'),
            'INDEX_NAME': 'haystack',
            'SETTINGS_NAME': 'cs',
            'DEFAULT_ANALYZER': 'czech_hunspell',
            'DEFAULT_NGRAM_SEARCH_ANALYZER': 'standard',
        },
    }

    ELASTICSEARCH_INDEX_SETTINGS = {
        'cs': {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "czech_hunspell": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["stopwords_CZ", "lowercase", "hunspell_CZ", "stopwords_CZ", "remove_duplicities"]
                        }
                    },
                    "filter": {
                        "stopwords_CZ": {
                            "type": "stop",
                            "stopwords": ["právě", "že", "test", "_czech_"],
                            "ignore_case": True
                        },
                        "hunspell_CZ": {
                            "type": "hunspell",
                            "locale": "cs_CZ",
                            "dedup": True,
                            "recursion_level": 0
                        },
                        "remove_duplicities": {
                            "type": "unique",
                            "only_on_same_position": True
                        },
                    }
                }
            }
        },
    }


Field based analysis
--------------------

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


Django CBV style views
----------------------

Haystacks's class based views predate the inclusion of CBVs into the Django
core and so the paradigms are different. This makes it harder to impossible to
make use of view mixins.

The bundled `SearchView` and `FacetedSearchView` classes are based on
`django.views.generic.edit.FormView` using the `SearchMixin` and
`FacetedSearchMixin`, respectively. The `SearchMixin` provides the necessary
search related attributes and overloads the form processing methods to execute
the search.

The `SearchMixin` adds a few search specific attributes:

* `load_all` - a Boolean value for `specifying database lookups <http://django-haystack.readthedocs.org/en/latest/searchqueryset_api.html#load-all>`_
* `queryset` - a default `SearchQuerySet`. Defaults to `EmtpySearchQuerySet`
* `search_field` - the name of the form field used for the query. This is added
  to allow for views which may have more than one search form. Defaults to `q`.

.. note::
    The `SearchMixin` uses the attribute named `queryset` for the resultant
    `SearchQuerySet`. Naming this attribute `searchqueryset` would make more
    sense semantically and hew closer to Haystack's naming convention, however
    by using the `queryset` attribute shared by other Django view mixins it is
    relatively easy to combine search functionality with other mixins and
    views.

Management commands
-------------------

show_mapping
~~~~~~~~~~~~

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
~~~~~~~~~~~~~

Provided the name of an indexed model and a key it generates and prints the
generated document for this object::

    python manage.py show_document myapp.MyModel 19181

The JSON document will be formatted with 'pretty' indenting.

Stability, docs, and tests
==========================

The form, view, and backend functionality in this project is considered stable.
Test coverage is not substantial, but is run against Django 1.4 through Django
1.6 on Python 2.6 and Python 2.7, Django 1.5 and Django 1.6 on Python 3.3, and
Django 1.6 on PyPy.

Why not add this stuff to Haystack?
-----------------------------------

This project first aims to solve problems related specifically to working with
ElasticSearch. Haystack is 1) backend agnostic (a good thing), 2) needs to
support existing codebases, and 3) not my project. Most importantly, adding
these features through a separate Django app means providing them without
needing to fork Haystack. Hopefully some of the features here, once finalized
and tested, will be suitable to add to Haystack.
