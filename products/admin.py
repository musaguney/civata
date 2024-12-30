from django.contrib import admin
from .models import Category, Product, Subscriber

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #prepopulated_fields = {"slug": ("name",)}
    list_display = ['id', 'name'] 
    list_display_links = ["id","name"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'fakeid', 'name', 'category', 'price', 'brand', 'quantity']
    list_display_links = ["name","id", 'fakeid']
    list_filter = ['category', 'brand', 'coating']
    search_fields = ['name', 'description', 'seo_title', 'seo_meta_keywords']
    prepopulated_fields = {"slug": ("name",)}
    
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)  # Admin panelinde görünecek sütunlar
