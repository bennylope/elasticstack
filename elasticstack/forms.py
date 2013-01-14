# A better search form will not require the use of a specifically named `q`
# field for search.

from django import forms
from django.utils.translation import ugettext_lazy as _
from haystack.query import SearchQuerySet, EmptySearchQuerySet


class SearchForm(forms.Form):
    q = forms.CharField(label=_('Search'))

    search_field_name = 'q'

    def __init__(self, *args, **kwargs):
        self.searchqueryset = kwargs.pop('searchqueryset', SearchQuerySet())
        self.load_all = kwargs.pop('load_all', False)
        super(SearchForm, self).__init__(*args, **kwargs)
        if self.search_field_name != 'q':
            self.fields.pop('q')

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return EmptySearchQuerySet()

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def get_suggestion(self):
        if not self.is_valid():
            return None

        return self.searchqueryset.spelling_suggestion(self.cleaned_data['q'])
