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

from haystack.fields import (CharField as BaseCharField,
        LocationField as BaseLocationField,
        NgramField as BaseNgramField,
        EdgeNgramField as BaseEdgeNgramField,
        IntegerField as BaseIntegerField,
        FloatField as BaseFloatField,
        DecimalField as BaseDecimalField,
        BooleanField as BaseBooleanField,
        DateField as BaseDateField,
        DateTimeField as BaseDateTimeField,
        MultiValueField as BaseMultiValueField,
        FacetField as BaseFacetField)


class ConfigurableFieldMixin(object):
    """
    A mixin which allows specifying the analyzer on a per field basis.
    """

    def __init__(self, **kwargs):
        self.analyzer = kwargs.pop('analyzer', None)
        if self.analyzer is None:
            raise ValueError("Configurable fields must have an analyzer type")
        super(ConfigurableFieldMixin, self).__init__(**kwargs)


class CharField(ConfigurableFieldMixin, BaseCharField):
    pass


class LocationField(ConfigurableFieldMixin, BaseLocationField):
    pass


class NgramField(ConfigurableFieldMixin, BaseNgramField):
    pass


class EdgeNgramField(ConfigurableFieldMixin, BaseEdgeNgramField):
    pass


class IntegerField(ConfigurableFieldMixin, BaseIntegerField):
    pass


class FloatField(ConfigurableFieldMixin, BaseFloatField):
    pass


class DecimalField(ConfigurableFieldMixin, BaseDecimalField):
    pass


class BooleanField(ConfigurableFieldMixin, BaseBooleanField):
    pass


class DateField(ConfigurableFieldMixin, BaseDateField):
    pass


class DateTimeField(ConfigurableFieldMixin, BaseDateTimeField):
    pass


class MultiValueField(ConfigurableFieldMixin, BaseMultiValueField):
    pass


class FacetField(ConfigurableFieldMixin, BaseFacetField):
    pass


class FacetCharField(FacetField, CharField):
    pass


class FacetIntegerField(FacetField, IntegerField):
    pass


class FacetFloatField(FacetField, FloatField):
    pass


class FacetDecimalField(FacetField, DecimalField):
    pass


class FacetBooleanField(FacetField, BooleanField):
    pass


class FacetDateField(FacetField, DateField):
    pass


class FacetDateTimeField(FacetField, DateTimeField):
    pass


class FacetMultiValueField(FacetField, MultiValueField):
    pass
