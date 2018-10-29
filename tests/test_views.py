#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_elasticstack
------------

Tests for `elasticstack` views module.
"""

from django.test import TestCase
from django.test.client import RequestFactory

from elasticstack import views


class TestElasticstack(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_form_kwargs(self):
        """Ensure request data updates the form kwargs"""
        request = self.factory.request()
        request.GET = {"q": "whoami"}

        mixin = views.SearchMixin()
        mixin.request = request
        mixin.queryset = []  # An EmptySearchQuerySet is basically an empty list

        self.assertEqual(
            mixin.get_form_kwargs(),
            {"initial": {}, "data": request.GET, "searchqueryset": []},
        )
