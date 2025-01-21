from django.urls import path
from .views import product_list, home, about, contact, product_detail, offline_page, category
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, CategorySitemap, ProductSitemap
from django.conf.urls import handler404
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404


sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
    
}

urlpatterns = [
    #path('menu/', menu_view, name='menu'),  # Menü görünümü
    path('offline/', offline_page, name='offline'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('category/', product_list, name='product_list'),
    path('category/<slug:category_slug>/', product_list, name='product_list_by_category'),  # Kategoriye göre ürünler
 
    path('', home, name='home'),  # Ana sayfa
    path('about/', about, name='about'),  # Hakkımızda sayfası
    path('contact/', contact, name='contact'),
    path('urunlerimiz/', category, name='category'),
]
