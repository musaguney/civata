from django_filters import FilterSet, CharFilter, ChoiceFilter
from .models import Product

class ProductFilter(FilterSet):
    product_type = ChoiceFilter(field_name='product_type', choices=Product.PRODUCT_TYPES, label='Ürün Çeşidi')
    category = CharFilter(field_name='category__name', lookup_expr='icontains', label='Kategori')
    diameter = CharFilter(field_name='diameter', lookup_expr='icontains', label='Çap')
    length = CharFilter(field_name='length', lookup_expr='icontains', label='Uzunluk')

    class Meta:
        model = Product
        fields = ['product_type', 'category', 'diameter', 'length']