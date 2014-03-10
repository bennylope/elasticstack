============
Installation
============

Base installation
=================

Installation is straightforward. With your `virtualenv
<http://www.virtualenv.org/en/latest/>`_ activated, use pip to install::

    $ pip install elasticstack

Then add `elasticstack` to your Django project's `INSTALLED_APPS`::

    INSTALLED_APPS = (
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "haystack",
        "elasticstack",
    ),

Adding the app to your `INSTALLED_APPS` is necessary to make the management
commands available.

Haystack connection settings
============================

In order to use the configurable ElasticSearch indexing settings you will need
to make sure that you're using the project defined backend. Change this::

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }

To this::

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'elasticstack.backends.ConfigurableElasticSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }

For a full explanation of why and how to customize your index settings, see the :doc:`/mappings` documentation.
