from django_filters import rest_framework as filters
from apps.geodata.models import Building


class BuildingFilter(filters.FilterSet):

    aoi = filters.CharFilter(field_name="aoi__name", lookup_expr='exact')
    address = filters.CharFilter(field_name="address", method='filter_address')
    uid = filters.CharFilter(field_name='uid', lookup_expr='exact')
    geohash = filters.CharFilter(field_name='geohash', lookup_expr='exact')

    class Meta:
        model = Building
        fields = ['aoi', 'address', 'uid', 'geohash']

    def filter_address(self, queryset, name, value):
        return queryset.filter(address__search=value)[0:10]
