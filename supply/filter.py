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
    product = filters.CharFilter(method="product")

    def shop_filter(self, queryset, name, value):
        """"""
        return queryset.filter(shop__idencode=decode('value'))

    def product_filter(self, queryset, name, value):
        """"""
        return queryset.filter(product__idencode=decode('value'))
