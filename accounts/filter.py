from django.db.models import Sum, F, Q, Case, When
from django_filters import rest_framework as filters

from accounts.models import Card
from common.functions import decode


class CardFilter(filters.FilterSet):
    """"""
    number = filters.NumberFilter(method="number_filter")
    verified = filters.BooleanFilter(method="verified_filter")

    def number_filter(self, queryset, name, value):
        return queryset.filter(card_number__icontains=value)

    def verified_filter(self, queryset, name, value):
        return queryset.filter(verified__icontains=value)


class ShopFilter(filters.FilterSet):
    """"""
    location = filters.NumberFilter(method="location_filter")
    verified = filters.BooleanFilter(method="verified_filter")

    def location_filter(self, queryset, name, value):
        return queryset.filter(location__icontains=value)

    def verified_filter(self, queryset, name, value):
        return queryset.filter(verified__icontains=value)
