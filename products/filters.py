from django_filters import FilterSet, CharFilter, ChoiceFilter
from .models import Product

class ProductFilter(FilterSet):
    product_type = ChoiceFilter(field_name='product_type', choices=Product.PRODUCT_TYPES, label='Ürün Çeşidi')
    title_type = CharFilter(field_name='title_type', lookup_expr='iexact', label='Kategori')
    diameter = CharFilter(field_name='diameter', lookup_expr='icontains', label='Çap')
    length = CharFilter(field_name='length', lookup_expr='icontains', label='Uzunluk')

    class Meta:
        model = Product
        fields = ['product_type', 'title_type', 'diameter', 'length']