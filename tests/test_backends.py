#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_elasticstack
------------

Tests for `elasticstack` backends module.
"""

from django.test import TestCase
from django.test.utils import override_settings

from haystack.fields import CharField as HaystackCharField

from elasticstack import backends
from elasticstack import fields


class TestBackendSettings(TestCase):
    """
    Basic tests that the backend replaces the attributes as expected.
    """

    @override_settings(ELASTICSEARCH_DEFAULT_ANALYZER="stop")
    def test_user_analyzer(self):
        """Ensure that the default analyzer is overridden"""
        back_class = backends.ConfigurableElasticBackend(
            'default', URL="http://localhost:9200", INDEX_NAME="")
        self.assertEqual(back_class.DEFAULT_ANALYZER, "stop")

    @override_settings(ELASTICSEARCH_INDEX_SETTINGS={"index": 4})
    def test_user_settings(self):
        """Ensure that the default index settings are overridden"""
        back_class = backends.ConfigurableElasticBackend(
            'default', URL="http://localhost:9200", INDEX_NAME="")
        self.assertEqual(back_class.DEFAULT_SETTINGS, {"index": 4})


class TestSchema(TestCase):
    """
    Tests that the schema is built using the specified settings.

    The backend class must be configured in each test method to ensure its
    settings are test specific.
    """

    def test_contral_analyzer(self):
        """Control test that the default analyzer is snowball"""
        back_class = backends.ConfigurableElasticBackend(
            'default', URL="http://localhost:9200", INDEX_NAME="")
        text_field = HaystackCharField(document=True, use_template=True,
                index_fieldname='body')
        # build_schema is passed a SortedDict of search index fields keyed by
        # field name
        schema = back_class.build_schema({'body': text_field})
        self.assertEqual("snowball", schema[1]['body']['analyzer'])

    @override_settings(ELASTICSEARCH_DEFAULT_ANALYZER="stop")
    def test_custom_analyzer(self):
        """Ensure custom analyzer used for fields"""
        back_class = backends.ConfigurableElasticBackend(
            'default', URL="http://localhost:9200", INDEX_NAME="")
        text_field = HaystackCharField(document=True, use_template=True,
                index_fieldname='body')
        # build_schema is passed a SortedDict of search index fields keyed by
        # field name
        schema = back_class.build_schema({'body': text_field})
        self.assertEqual("stop", schema[1]['body']['analyzer'])

    def test_field_analyzer(self):
        """Ensure that field analyzer works on a case by case basis"""
        back_class = backends.ConfigurableElasticBackend(
            'default', URL="http://localhost:9200", INDEX_NAME="")
        # Control test - by default the CharField does not have a keyword
        # argument named 'analyzer' and does not take **kwargs
        self.assertRaises(TypeError, HaystackCharField, document=True,
                          use_template=True, index_fieldname='body', analyzer='stop')
        text_field = fields.CharField(document=True, use_template=True,
                index_fieldname='body', analyzer='stop')
        schema = back_class.build_schema({'body': text_field})
        self.assertEqual("stop", schema[1]['body']['analyzer'])
