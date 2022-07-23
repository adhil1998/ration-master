from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):
    """"""
    name = filters.CharFilter(method="name_filter")

    def name_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

