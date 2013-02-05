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
