from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Count
from .models import Product
from .models import Category
from .filters import ProductFilter
from django.http import JsonResponse
from .cart_manager import CartManager


def home(request):
    """Ana sayfa görünümü."""
    products = Product.objects.all()  # Ana sayfa için ürünler
    return render(request, 'index.html', {'products': products})
   
   
def sepet(request):
    """Sepet sayfasını görüntüler."""
    cart_manager = CartManager(request)
    cart_summary = cart_manager.get_cart_summary()
    return render(request, 'sepet.html', {'cart': cart_summary})

def add_to_cart(request, product_id):
    cart_manager = CartManager(request)
    try:
        cart_manager.add_to_cart(product_id)
        return JsonResponse({
            'success': True,
            'message': 'Ürün başarıyla sepete eklendi.',
            'cart': cart_manager.get_cart_summary()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
def update_cart(request, product_id, action):
    """Sepette ürün miktarını artırır veya azaltır."""
    cart_manager = CartManager(request)
    if action == 'increment':
        cart_manager.add_to_cart(product_id)
    elif action == 'decrement':
        cart_manager.update_quantity(product_id, increment=False)
    return JsonResponse({'success': True, 'cart': cart_manager.get_cart_summary()})

def remove_from_cart(request, product_id):
    """Sepetten bir ürünü kaldırır."""
    cart_manager = CartManager(request)
    cart_manager.remove_from_cart(product_id)
    return JsonResponse({'success': True, 'cart': cart_manager.get_cart_summary()})

def clear_cart(request):
    """Sepeti tamamen temizler."""
    request.session['cart'] = {}
    request.session.modified = True
    return JsonResponse({'success': True})

# Sabit çap ve uzunluk seçenekleri
DIAMETER_CHOICES = [
    ('m4', 'M4'), ('m6', 'M6'), ('m8', 'M8'), ('m10', 'M10'), ('m12', 'M12'),
]

LENGTH_CHOICES = [
    ('30mm', '30mm'), ('40mm', '40mm'), ('50mm', '50mm'), ('60mm', '60mm'),
    ('70mm', '70mm'), ('80mm', '80mm'), ('90mm', '90mm'), ('100mm', '100mm'),
    ('110mm', '110mm'), ('120mm', '120mm'), ('130mm', '130mm'),
    ('140mm', '140mm'), ('150mm', '150mm'),
]

def product_list(request):
    # Tüm ürünleri al
    products = Product.objects.all()

    # Django Filter ile filtreleme
    filter_set = ProductFilter(request.GET, queryset=products)
    filtered_products = filter_set.qs
    
    # Sıralama bilgisi al
    sort_option = request.GET.get('sort', '')
    if sort_option == 'name_asc':
        filtered_products = filtered_products.order_by('name')
    elif sort_option == 'name_desc':
        filtered_products = filtered_products.order_by('-name')
    elif sort_option == 'price_asc':
        filtered_products = filtered_products.order_by('price')
    elif sort_option == 'price_desc':
        filtered_products = filtered_products.order_by('-price')
    
    # Eğer filtreleme yapılmadıysa tüm ürünleri varsayılan sırayla göster
    if not request.GET:
        filtered_products = filtered_products.order_by('id')

    # Sayfalama (Paginator)
    paginator = Paginator(filtered_products, 15)  # Sayfa başına 15 ürün
    page_number = request.GET.get('page')  # URL'deki 'page' parametresini al
    page_obj = paginator.get_page(page_number)

    # Çap sayısını hesapla ve sabit seçeneklerle birleştir
    diameter_counts_db = products.values('diameter').annotate(count=Count('diameter'))
    diameter_counts_db = {item['diameter']: item['count'] for item in diameter_counts_db}
    diameter_counts = []
    for diameter, label in DIAMETER_CHOICES:
        diameter_counts.append({
            'diameter': diameter,
            'label': label,
            'count': diameter_counts_db.get(diameter, 0)  # Veritabanında yoksa 0
        })

    # Uzunluk sayısını hesapla ve sabit seçeneklerle birleştir
    length_counts_db = products.values('length').annotate(count=Count('length'))
    length_counts_db = {item['length']: item['count'] for item in length_counts_db}
    length_counts = []
    for length, label in LENGTH_CHOICES:
        length_counts.append({
            'length': length,
            'label': label,
            'count': length_counts_db.get(length, 0)  # Veritabanında yoksa 0
        })

    # Filtreleme seçeneklerini oluştur
    product_type_counts = products.values('product_type').annotate(count=Count('product_type'))
    title_type_counts = products.values('title_type').annotate(count=Count('title_type'))
    
     # Seçimlerin alınması
    selected_filters = {
        'product_type': request.GET.get('product_type', 'Hepsi'),
        'title_type': request.GET.get('title_type', 'Hepsi'),
        'diameter': request.GET.get('diameter', 'Hepsi'),
        'length': request.GET.get('length', 'Hepsi'),
    }

    return render(request, 'product_list.html', {
        'filter': filter_set,
        'page_obj': page_obj,  # Sayfalama nesnesi
        'product_type_counts': product_type_counts,
        'title_type_counts': title_type_counts,
        'diameter_counts': diameter_counts,
        'length_counts': length_counts,
        'selected_filters': selected_filters,  # Seçimleri template'e gönder
        'sort_option': sort_option,  # Seçimi template'e gönder
    })
 
