# Copyright (c) 2014-2015, Ben Lopatin
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.  Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with
# the distribution

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django import forms
from django.utils.translation import ugettext_lazy as _

from haystack.query import SearchQuerySet


class SearchForm(forms.Form):
    """
    A search form that does not require the use of a specifically named `q`
    field for search.

    Another field can be substituted provided that it is identified using the
    `search_field_name` attribute.
    """
    q = forms.CharField(label=_('Search'))

    search_field_name = 'q'

    def __init__(self, *args, **kwargs):
        self.searchqueryset = kwargs.pop('searchqueryset', SearchQuerySet())
        self.load_all = kwargs.pop('load_all', False)
        super(SearchForm, self).__init__(*args, **kwargs)
        if self.search_field_name != 'q':
            self.fields.pop('q')

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get(self.search_field_name):
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data[self.search_field_name])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def get_suggestion(self):
        if not self.is_valid():
            return None

        return self.searchqueryset.spelling_suggestion(self.cleaned_data[self.search_field_name])
