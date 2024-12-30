from .models import Category

def footer_context(request):
    """
    Footer için gerekli olan bilgileri sağlayan context processor.
    """
    categories = Category.objects.all()  # Kategorileri al
    contact_info = {
        "address": "İkitelli OSB, İPKAS Plastikçiler Sanayi Sitesi, 3B Blok No:32 Başakşehir/ İstanbul",
        "email": "info@kiliccivata.com",
        "phone": "+90 212 549 34 55",
        "whatsapp": "+90 533 264 65 98",
    }
    social_links = {
        "instagram": "https://www.instagram.com/kilic_civata_vida_baglanti/",
        "facebook": "https://www.facebook.com/Civatacim",
        "email": "mailto:info@kiliccivata.com",
        "sitemap": "/sitemap.xml",
    }
    return {
        "categories": categories,
        "contact_info": contact_info,
        "social_links": social_links,
    }

def menu_data(request):
    # Tüm kategorileri ve ilişkili ürünleri al
    categories = Category.objects.prefetch_related('products').all()

    menu_data = []
    for category in categories:
        products = category.products.all()  # Bu kategoriye ait tüm ürünler
        first_product = products.first()  # İlk ürünü al
        menu_data.append({
            'category': category,
            'products': products,
            'first_product_image': first_product.main_image.url if first_product and first_product.main_image else None,
            'title_type': first_product.title_type if first_product and hasattr(first_product, 'title_type') else None,
        })

    # Menü verisini döndür
    return {'menu_data': menu_data}


def index_product(request):
    # Tüm kategorileri ve ilişkili ürünleri al
    categories = Category.objects.prefetch_related('products')

    index_product = []
    for category in categories:
        products = category.products.all()[:2]  # Her kategoriden yalnızca 2 ürün al
        if products:  # Eğer ürün varsa işleme devam et
            index_product.extend([
                {
                    'id': product.id,
                    'slug': product.slug,
                    'name': product.name,
                    'image': product.main_image.url if product.main_image else None,
                    'product_type': product.product_type or 'Bilinmiyor',
                    'title_type': product.title_type or 'Bilinmiyor',
                    'diameter': product.diameter or 'Belirtilmemiş',
                    'length': product.length or 'Belirtilmemiş',
                    'coating': product.coating or 'Yok',
                    'material': product.material or 'Belirtilmemiş',
                    'strength_class': product.strength_class or 'Belirtilmemiş',
                    'brand': product.brand or 'Bilinmiyor',
                    'quantity': product.quantity if product.quantity else 0,
                    'price': f"{product.price:.2f}" if product.price else 'Teklif Alın',
                    'trendyol_link': product.trendyol_link or '#',
                }
                for product in products
            ])
    
    return {'index_product': index_product}