============
elasticstack
============

:Version: 0.0.4
:Status: alpha
:Author: Ben Lopatin (http://benlopatin.com)

Configurable indexing and other extras for Haystack (with ElasticSearch
biases).

Requirements
============

* `Django <https://www.djangoproject.com/>`_: the features in elasticstack have
  only been tested on 1.4.x.
* `Haystack <http://www.haystacksearch.org/>`_: ElasticSearch support was only
  added in Haystack 2.x which is still in development. You'll need to install
  Haystack from source.
* `ElasticSearch <http://www.elasticsearch.org/>`_: presumably any newish
  version will do, however the only version tested against so far is 0.19.x

Features and goals
==================

Some of these features are backend agnostic but most features have
ElasticSearch in mind.

For more background see the blog post `Stretching Haystack's ElasticSearch
Backend
<http://www.wellfireinteractive.com/blog/custom-haystack-elasticsearch-backend/>`_.

Configurable index mapping
--------------------------

The search mapping provided by Haystack's ElasticSearch backend includes brief
but sensible defaults for nGram analysis. You can add change these settings or
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

The default analyzer for non-nGram fields in Haystack's ElasticSearch backend
is the `snowball analyzer
<http://www.elasticsearch.org/guide/reference/index-modules/analysis/snowball-analyzer.html>`_.
A perfectly good analyzer but not necessarily what you need. It's also language
specific (English by default).

Specify your analyzer with `ELASTICSEARCH_DEFAULT_ANALYZER` in your settings
file::

    ELASTICSEARCH_DEFAULT_ANALYZER = 'synonym_analyzer'

Now all your analyzed fields, except for nGram fields, will be analyzed using
`synonym_analyzer`.

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

show_document
~~~~~~~~~~~~~

Provided the name of an indexed model and a key it generates and prints the
generated document for this object::

    python manage.py show_document myapp.MyModel 19181

The JSON document will be formatted with 'pretty' indenting.

Stability, docs, and tests
==========================

This project is in 'alpha'! Index control *should* remain fairly stable but
everything should be considred subject to change until beta. As of yet, no docs
(see the aforementioned blog post to get started) and no tests (hold on to your
butts).

Why not add this stuff to Haystack?
-----------------------------------

This project first aims to solve problems related specifically to working with
ElasticSearch. Haystack is 1) backend agnostic (a good thing), 2) needs to
support existing codebases, and 3) not my project. Most importantly, adding
these features through a separate Django app means providing them without
needing to fork Haystack. Hopefully some of the features here, once finalized
and tested, will be suitable to add to Haystack.
