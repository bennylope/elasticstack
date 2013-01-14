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
