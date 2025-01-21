from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SubscriptionForm
from django.db.models import Count
from .models import Product
from .models import Category
from .filters import ProductFilter
from django.http import JsonResponse
from .cart_manager import CartManager
import json
from itertools import groupby

def category(request):
    """Ürünleri ID sırasına göre al ve title_type'a göre gruplandır"""
    
    # Tüm ürünleri ID sırasına göre çek
    products = Product.objects.all().order_by('id')

    # Eksik ID'ler olabilir ama sıralama korunur
    grouped_products = {}
    for title_type, items in groupby(products, key=lambda x: x.title_type):
        grouped_products[title_type] = list(items)

    return render(request, 'category.html', {'grouped_products': grouped_products})


def offline_page(request):
    return render(request, 'assets/offline.html')

def product_detail(request, slug):
    # İlgili ürünü getir
    product = get_object_or_404(Product, slug=slug)
    
    # Tüm ürünleri al
    all_products = Product.objects.all()
    filtered_products = [
        {
            'id': urun.id,
            'name': urun.name,
            'title_type': urun.title_type,
            'price': urun.price,
            'slug': urun.slug,
            'main_image': urun.main_image.url if urun.main_image else None,
            'quantity': urun.quantity,
            'measures': urun.measures,
        }
        for urun in all_products if urun.id != product.id
    ]
    return render(request, 'product_detail.html', {
        'product': product,
        'all_products': filtered_products,
    })
    

def about(request):
    """Hakkımızda sayfası görünümü."""
    return render(request, 'about.html')

def contact(request):
    """iletişim sayfası görünümü."""
    return render(request, 'contact.html')
 
def home(request):
    """Ana sayfa görünümü."""
    products = Product.objects.all()  # Ana sayfa için ürünler

    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "E-bültene başarıyla abone oldunuz!")
            return redirect('home')  # Ana sayfaya yönlendirme
    else:
        form = SubscriptionForm()
        
    products = Product.objects.all().order_by('id')

    # Eksik ID'ler olabilir ama sıralama korunur
    grouped_products = {}
    for title_type, items in groupby(products, key=lambda x: x.title_type):
        grouped_products[title_type] = list(items)

    return render(request, 'index.html', {'products': products, 'form': form, 'grouped_products': grouped_products})
   
   


def product_list(request, category_slug=None):
    # Kategori kontrolü
    category = None
    if category_slug:
        category = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    # Django Filter ile filtreleme
    filter_set = ProductFilter(request.GET, queryset=products)
    filtered_products = filter_set.qs

    # title_type ile filtreleme
    title_type_filter = request.GET.get('title_type', '')
    if title_type_filter and title_type_filter != 'Hepsi':
        filtered_products = filtered_products.filter(title_type=title_type_filter)

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

    # Sayfalama (Paginator)
    paginator = Paginator(filtered_products, 15)  # Sayfa başına 15 ürün
    page_number = request.GET.get('page')  # URL'deki 'page' parametresini al
    page_obj = paginator.get_page(page_number)

    # title_type sayısını hesapla
    title_type_counts = products.values('title_type').annotate(count=Count('title_type'))

    # Seçimlerin alınması
    selected_filters = {
        'title_type': title_type_filter,

    }

    return render(request, 'product_list.html', {
        'filter': filter_set,
        'page_obj': page_obj,  # Sayfalama nesnesi
        'category': category,  # Seçili kategori
        'title_type_counts': title_type_counts,
        'selected_filters': selected_filters,  # Seçimleri template'e gönder
        'sort_option': sort_option,  # Seçimi template'e gönder
        
    })