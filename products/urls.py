from django.urls import path
from .views import product_list, sepet, add_to_cart, update_cart, remove_from_cart, clear_cart, home, about, contact, product_detail, offline_page
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ProductSitemap
from django.conf.urls import handler404
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404


sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    #path('menu/', menu_view, name='menu'),  # Menü görünümü
    path('offline/', offline_page, name='offline'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('category/', product_list, name='product_list'),
    path('sepet/', sepet, name='sepet'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/<str:action>/', update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('', home, name='home'),  # Ana sayfa
    path('about/', about, name='about'),  # Hakkımızda sayfası
    path('contact/', contact, name='contact'),
]
