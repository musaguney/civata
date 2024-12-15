import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import shutil
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField

def product_main_image_upload_path(instance, filename):
    """Ana resim dosyasını productmain/{fakeid}/ altına yükler."""
    return f"productmain/{instance.fakeid}/{filename}"


def product_additional_image_upload_path(instance, filename):
    """Ek resimleri productdetail/{fakeid}/ altına yükler."""
    return f"productdetail/{instance.fakeid}/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    PRODUCT_TYPES = [
        ('Vida', 'Vida'),
        ('Civata', 'Civata'),
        ('Saplama', 'Saplama'),
    ]
    
    
    id = models.AutoField(primary_key=True)
    fakeid = models.PositiveIntegerField(unique=True, verbose_name="Fake ID")  # Fake ID alanı
    name = models.CharField(max_length=255)
    isoname = models.CharField(max_length=255, default="ISO", verbose_name="İso Adı")
    dinname = models.CharField(max_length=255, default="DIN", verbose_name="Din Adı")
    slug = models.SlugField(unique=True, verbose_name="SEO URL")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=255, choices=PRODUCT_TYPES, verbose_name="Ürün Çeşidi")
    title_type = models.CharField(max_length=255, verbose_name="Başlık Tipi")
    
    diameter = models.CharField(max_length=10, choices=[
        ('m6', 'M6'), ('m8', 'M8'), ('m10', 'M10'), ('m12', 'M12')
    ], verbose_name="Çap")
    length = models.CharField(max_length=10, choices=[
        ('30mm', '30mm'), ('40mm', '40mm'), ('50mm', '50mm'), ('60mm', '60mm'),
        ('70mm', '70mm'), ('80mm', '80mm'), ('90mm', '90mm'), ('100mm', '100mm'),
        ('110mm', '110mm'), ('120mm', '120mm'), ('130mm', '130mm'),
        ('140mm', '140mm'), ('150mm', '150mm')
    ], verbose_name="Uzunluk")
    coating = models.CharField(max_length=20, choices=[
        ('Yok', 'Yok'), ('Var (Zn Cr+3)', 'Var (Zn Cr+3)')
    ], verbose_name="Kaplama")
    material = models.CharField(max_length=255, verbose_name="Malzeme")
    strength_class = models.CharField(max_length=255, verbose_name="Dayanım Sınıfı")
    brand = models.CharField(max_length=255, default="Kılıç Civata", verbose_name="Marka")
    quantity = models.PositiveIntegerField(verbose_name="Adet Miktarı")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")
    description = RichTextUploadingField(verbose_name="Açıklama Metni")
    trendyol_link = models.URLField(blank=True, verbose_name="Trendyol Linki")

    # Resimler
    main_image = models.ImageField(upload_to=product_main_image_upload_path, verbose_name="Ana Resim (516x480)")
    additional_image1 = models.ImageField(upload_to=product_additional_image_upload_path, null=True, blank=True, verbose_name="Ek Resim 1 (1272x1272)")
    additional_image2 = models.ImageField(upload_to=product_additional_image_upload_path, null=True, blank=True, verbose_name="Ek Resim 2 (1272x1272)")
    additional_image3 = models.ImageField(upload_to=product_additional_image_upload_path, null=True, blank=True, verbose_name="Ek Resim 3 (1272x1272)")
    additional_image4 = models.ImageField(upload_to=product_additional_image_upload_path, null=True, blank=True, verbose_name="Ek Resim 4 (1272x1272)")
    additional_image5 = models.ImageField(upload_to=product_additional_image_upload_path, null=True, blank=True, verbose_name="Ek Resim 5 (1272x1272)")
    additional_image6 = models.ImageField(upload_to=product_additional_image_upload_path, null=True, blank=True, verbose_name="Ek Resim 6 (1272x1272)")
    additional_image7 = models.ImageField(upload_to=product_additional_image_upload_path, null=True, blank=True, verbose_name="Ek Resim 7 (1272x1272)")

    seo_title = models.CharField(max_length=255, verbose_name="SEO Başlığı")
    seo_meta_description = models.TextField(verbose_name="Meta Açıklaması", blank=True, null=True)
    seo_meta_keywords = models.CharField(max_length=255, verbose_name="Meta Anahtar Kelimeler", blank=True, null=True)
    seo_meta_author = models.CharField(max_length=255, verbose_name="Meta Yazar", default="Kılıç Civata")

    def __str__(self):
        return self.name
    


@receiver(post_delete, sender=Product)
def delete_product_files(sender, instance, **kwargs):
    """Ürün silindiğinde dosyalarını ve klasörlerini temizler."""
    main_image_path = os.path.join(settings.MEDIA_ROOT, f"productmain/{instance.fakeid}")
    additional_image_path = os.path.join(settings.MEDIA_ROOT, f"productdetail/{instance.fakeid}")

    # Ana resim klasörünü sil
    if os.path.exists(main_image_path):
        shutil.rmtree(main_image_path)

    # Ek resim klasörünü sil
    if os.path.exists(additional_image_path):
        shutil.rmtree(additional_image_path)   
      
        
    class Meta:
        ordering = ['id']