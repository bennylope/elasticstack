======================
Django CBV style views
======================

Haystacks's class based views predate the inclusion of CBVs into the Django
core and so the paradigms are different. This makes it harder to impossible to
make use of view mixins.

The bundled `SearchView` and `FacetedSearchView` classes are based on
`django.views.generic.edit.FormView` using the `SearchMixin` and
`FacetedSearchMixin`, respectively. The `SearchMixin` provides the necessary
search related attributes and overloads the form processing methods to execute
the search.

The `SearchMixin` adds a few search specific attributes:

* `load_all` - a Boolean value for `specifying database lookups <http://django-haystack.readthedocs.org/en/latest/searchqueryset_api.html#load-all>`_
* `queryset` - a default `SearchQuerySet`. Defaults to `EmtpySearchQuerySet`
* `search_field` - the name of the form field used for the query. This is added
  to allow for views which may have more than one search form. Defaults to `q`.

.. note::
    The `SearchMixin` uses the attribute named `queryset` for the resultant
    `SearchQuerySet`. Naming this attribute `searchqueryset` would make more
    sense semantically and hew closer to Haystack's naming convention, however
    by using the `queryset` attribute shared by other Django view mixins it is
    relatively easy to combine search functionality with other mixins and
    views.
