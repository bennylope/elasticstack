#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_elasticstack
------------

Tests for `elasticstack` forms module.
"""

from django import forms
from django.test import TestCase

from elasticstack.forms import SearchForm


class TestForms(TestCase):

    def test_named_search_field(self):
        """Ensure that the `q` field can be optionally used"""

        class MyForm(SearchForm):
            s = forms.CharField(label="Search")
            f = forms.CharField(label="More search")
            search_field_name = "s"

        form = MyForm()
        self.assertTrue("s" in form.fields)
        self.assertFalse("q" in form.fields)
