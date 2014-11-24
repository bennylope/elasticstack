#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fields
------------

Tests for `elasticstack` fields module.
"""

from django.test import TestCase

from elasticstack.fields import ConfigurableFieldMixin


class TestFields(TestCase):

    def test_missing_analyzer(self):
        """No specified analyzer should result in an error"""
        self.assertRaises(ValueError, ConfigurableFieldMixin)
