from django_filters import FilterSet, CharFilter, ChoiceFilter
from .models import Product

class ProductFilter(FilterSet):
    
    title_type = CharFilter(field_name='title_type', lookup_expr='iexact', label='Kategori')
    

    class Meta:
        model = Product
        fields = ['title_type']