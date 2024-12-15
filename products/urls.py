from django.urls import path
from .views import product_list, sepet, add_to_cart, update_cart, remove_from_cart, clear_cart, home


urlpatterns = [
    #path('menu/', menu_view, name='menu'),  # Menü görünümü
    path('filter/', product_list, name='product_list'),
    path('sepet/', sepet, name='sepet'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/<str:action>/', update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('', home, name='home'),  # Ana sayfa
    
]
