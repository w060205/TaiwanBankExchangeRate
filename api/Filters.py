import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name="date", lookup_expr='lte')
    currency = django_filters.CharFilter(field_name="currency", lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['currency']
