import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import shutil
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.urls import reverse

def product_main_image_upload_path(instance, filename):
    """Ana resim dosyasını productmain/{fakeid}/ altına yükler."""
    return f"productmain/{instance.fakeid}/{filename}"


def product_additional_image_upload_path(instance, filename):
    """Ek resimleri productdetail/{fakeid}/ altına yükler."""
    return f"productdetail/{instance.fakeid}/{filename}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
class Category(models.Model):
    name = models.CharField(max_length=255)
    category_slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # category_slug otomatik olarak doldurulur
        if not self.category_slug:
            self.category_slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
  
    
    
    id = models.AutoField(primary_key=True)
    fakeid = models.PositiveIntegerField(unique=True, verbose_name="Fake ID")  # Fake ID alanı
    name = models.CharField(max_length=255)
    isoname = models.CharField(max_length=255, default="ISO standartlarına uygun üretilmiştir.", verbose_name="İso Adı")
    dinname = models.CharField(max_length=255, default="DIN standartlarına uygun üretilmiştir.", verbose_name="Din Adı")
    slug = models.SlugField(unique=True, verbose_name="SEO URL")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title_type = models.CharField(
        default="boş bırak",
        max_length=255,
        verbose_name="title_type",
        blank=True, 
        null=True
    )
    
    
    coating = models.CharField(max_length=20, choices=[
        ('Yok', 'Yok'), ('Var (Zn Cr⁺³)', 'Var (Zn Cr⁺³)')
    ], verbose_name="Kaplama")
    material = models.CharField(max_length=255, default="Soğuk şekillendirme çeliği", verbose_name="Malzeme")
    strength_class = models.CharField(max_length=255, default="4.6 dan 6.8'e", verbose_name="Dayanım Sınıfı")
    brand = models.CharField(max_length=255, default="Kılıç Civata", verbose_name="Marka")
    quantity = models.PositiveIntegerField(default="500", verbose_name="Adet Miktarı")
    price = models.DecimalField(max_digits=10, decimal_places=2, default="0", verbose_name="Fiyat")
    description_first = RichTextUploadingField(default="ilk açıklama metniiii", verbose_name="ilk açıklama metni")
    description = RichTextUploadingField(verbose_name="Açıklama Metni")
    trendyol_link = models.URLField(blank=True, default="https://www.trendyol.com/sr?mid=1004242&os=1", verbose_name="Trendyol Linki")

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
    updated_at = models.DateTimeField(auto_now=True)
    diameters = models.TextField(
        blank=True,
        null=True,
        verbose_name="Çaplar",
        help_text="Çap değerlerini virgülle ayırarak girin. Örnek: m6, m8, m10"
    )
    lengths = models.TextField(
        blank=True, null=True,
        verbose_name="Uzunluklar",
        help_text="Uzunluk değerlerini virgülle ayırarak girin. Örnek: 40mm, 50mm, 60mm"
    )
    measures = models.TextField(
        blank=True, null=True,
        verbose_name="Ölçüler",
        help_text="Ölçü değerlerini virgülle ayırarak girin. Örnek: 6x70, 8x90"
    )

    def get_diameters(self):
        return self.diameters.split(',')

    def get_lengths(self):
        return self.lengths.split(',')

    def get_measures(self):
        return self.measures.split(',')
    
    
    def get_absolute_url(self):
        # Product detay sayfasının URL'sini döndürür
        return reverse('product_detail', kwargs={'slug': self.slug})

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