from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category

# Statik sayfalar için Sitemap
class StaticViewSitemap(Sitemap):
    changefreq = "monthly"  # Güncellenme sıklığı
    priority = 0.8          # Öncelik seviyesi

    def items(self):
        # Statik sayfa URL isimlerini döndür
        return ['home', 'about', 'contact', 'product_list']

    def location(self, item):
        # URL isimlerini tam yollarına dönüştür
        return reverse(item)


# Dinamik kategoriler için Sitemap
class CategorySitemap(Sitemap):
    changefreq = "weekly"  # Güncellenme sıklığı
    priority = 0.7         # Öncelik seviyesi

    def items(self):
        # Tüm kategorileri döndür
        return Category.objects.all()

    def location(self, obj):
        # Kategorinin URL'sini oluştur
        return reverse('product_list_by_category', args=[obj.category_slug])


# Dinamik ürünler için Sitemap
class ProductSitemap(Sitemap):
    changefreq = "daily"  # Güncellenme sıklığı
    priority = 0.9        # Öncelik seviyesi

    def items(self):
        # Tüm ürünleri döndür
        return Product.objects.all()

    def lastmod(self, obj):
        # Ürünün en son güncellendiği tarih
        return obj.updated_at

    def location(self, obj):
        # Ürünün URL'sini oluştur
        return obj.get_absolute_url()