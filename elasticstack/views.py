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

from django.conf import settings
from django.core.paginator import Paginator
from django.views.generic import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin

from haystack.forms import ModelSearchForm, FacetedSearchForm
from haystack.query import EmptySearchQuerySet


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


class SearchMixin(MultipleObjectMixin, FormMixin):
    """
    A mixin that allows adding in Haystacks search functionality into
    another view class.

    This mixin exhibits similar end functionality as the base Haystack search
    view, but with some important distinctions oriented around greater
    compatibility with Django's built-in class based views and mixins.

    Normal flow:

        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()

    This mixin should:
        1. Make the form
        2. Get the queryset
        3. Return the paginated queryset

    """
    template_name = 'search/search.html'
    load_all = True
    form_class = ModelSearchForm
    queryset = EmptySearchQuerySet()
    context_object_name = None
    paginate_by = RESULTS_PER_PAGE
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = 'page'
    form_name = 'form'
    search_field = 'q'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        kwargs.update({'searchqueryset': self.get_query_set()})
        return kwargs

    def get_query_set(self):
        return self.queryset

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(**{
            self.form_name: form,
            'object_list': self.get_query_set()}))

    def form_valid(self, form):
        self.queryset = form.search()
        return self.render_to_response(self.get_context_data(**{
            self.form_name: form,
            'query': form.cleaned_data.get(self.search_field),
            'object_list': self.queryset}))


class FacetedSearchMixin(SearchMixin):
    """
    A mixin that allows adding in a Haystack search functionality with search
    faceting.
    """
    form_class = FacetedSearchForm

    def get_form_kwargs(self):
        kwargs = super(SearchMixin, self).get_form_kwargs()
        kwargs.update({'selected_facets': self.request.GET.getlist("selected_facets")})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(FacetedSearchMixin, self).get_context_data(**kwargs)
        context.update({'facets': self.results.facet_counts()})
        return context


class SearchView(SearchMixin, FormView):
    """A view class for searching a Haystack managed search index"""

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class FacetedSearchView(FacetedSearchMixin, SearchView):
    """
    A view class for searching a Haystack managed search index with
    facets
    """
    pass
