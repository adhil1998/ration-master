from django_filters import rest_framework as filters

from common.functions import decode


class ProductFilter(filters.FilterSet):
    """"""
    name = filters.CharFilter(method="name_filter")

    def name_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


class StockFilter(filters.FilterSet):
    """"""
    shop = filters.CharFilter(method="shop_filter")
    product = filters.CharFilter(method="product_filter")

    def shop_filter(self, queryset, name, value):
        """"""
        return queryset.filter(shop__id=decode(value))

    def product_filter(self, queryset, name, value):
        """"""
        return queryset.filter(product__id=decode(value))


class TokenFilter(filters.FilterSet):
    """"""
    date = filters.DateFilter(method='date_filter')
    shop = filters.CharFilter(method='shop_filter')
    status = filters.CharFilter(method='status_filter')

    def date_filter(self, queryset, name, value):
        """"""
        return queryset.filter(
            time__month=value.month, time__year=value.year, time__day=value.day)

    def shop_filter(self, queryset, name, value):
        """"""
        return queryset.filter(shop__id=decode(value))

    def status_filter(self, queryset, name, value):
        """"""
        return queryset.filter(status=value)
