============
elasticstack
============

:Version: 0.0.1
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

* Configurable indexing, from the project level to the field level
* Class based views more like Django CBV's
* Indexing and debugging helpers

Some of these features are backend agnostic but most features have
ElasticSearch in mind.

For more background see the blog post `Stretching Haystack's ElasticSearch
Backend
<http://www.wellfireinteractive.com/blog/custom-haystack-elasticsearch-backend/>`_.

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
