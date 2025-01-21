# Generated by Django 5.1.3 on 2025-01-11 11:25

import ckeditor_uploader.fields
import django.db.models.deletion
import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category_slug', models.SlugField(blank=True, max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fakeid', models.PositiveIntegerField(unique=True, verbose_name='Fake ID')),
                ('name', models.CharField(max_length=255)),
                ('isoname', models.CharField(default='ISO standartlarına uygun üretilmiştir.', max_length=255, verbose_name='İso Adı')),
                ('dinname', models.CharField(default='DIN standartlarına uygun üretilmiştir.', max_length=255, verbose_name='Din Adı')),
                ('slug', models.SlugField(unique=True, verbose_name='SEO URL')),
                ('title_type', models.CharField(blank=True, default='boş bırak', max_length=255, null=True, verbose_name='title_type')),
                ('coating', models.CharField(choices=[('Yok', 'Yok'), ('Var (Zn Cr+3)', 'Var (Zn Cr+3)')], max_length=20, verbose_name='Kaplama')),
                ('material', models.CharField(default='Soğuk şekillendirme çeliği', max_length=255, verbose_name='Malzeme')),
                ('strength_class', models.CharField(default="4.6 dan 6.8'e", max_length=255, verbose_name='Dayanım Sınıfı')),
                ('brand', models.CharField(default='Kılıç Civata', max_length=255, verbose_name='Marka')),
                ('quantity', models.PositiveIntegerField(default='500', verbose_name='Adet Miktarı')),
                ('price', models.DecimalField(decimal_places=2, default='0', max_digits=10, verbose_name='Fiyat')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Açıklama Metni')),
                ('trendyol_link', models.URLField(blank=True, default='https://www.trendyol.com/sr?mid=1004242&os=1', verbose_name='Trendyol Linki')),
                ('main_image', models.ImageField(upload_to=products.models.product_main_image_upload_path, verbose_name='Ana Resim (516x480)')),
                ('additional_image1', models.ImageField(blank=True, null=True, upload_to=products.models.product_additional_image_upload_path, verbose_name='Ek Resim 1 (1272x1272)')),
                ('additional_image2', models.ImageField(blank=True, null=True, upload_to=products.models.product_additional_image_upload_path, verbose_name='Ek Resim 2 (1272x1272)')),
                ('additional_image3', models.ImageField(blank=True, null=True, upload_to=products.models.product_additional_image_upload_path, verbose_name='Ek Resim 3 (1272x1272)')),
                ('additional_image4', models.ImageField(blank=True, null=True, upload_to=products.models.product_additional_image_upload_path, verbose_name='Ek Resim 4 (1272x1272)')),
                ('additional_image5', models.ImageField(blank=True, null=True, upload_to=products.models.product_additional_image_upload_path, verbose_name='Ek Resim 5 (1272x1272)')),
                ('additional_image6', models.ImageField(blank=True, null=True, upload_to=products.models.product_additional_image_upload_path, verbose_name='Ek Resim 6 (1272x1272)')),
                ('additional_image7', models.ImageField(blank=True, null=True, upload_to=products.models.product_additional_image_upload_path, verbose_name='Ek Resim 7 (1272x1272)')),
                ('seo_title', models.CharField(max_length=255, verbose_name='SEO Başlığı')),
                ('seo_meta_description', models.TextField(blank=True, null=True, verbose_name='Meta Açıklaması')),
                ('seo_meta_keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta Anahtar Kelimeler')),
                ('seo_meta_author', models.CharField(default='Kılıç Civata', max_length=255, verbose_name='Meta Yazar')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('diameters', models.TextField(blank=True, help_text='Çap değerlerini virgülle ayırarak girin. Örnek: m6, m8, m10', null=True, verbose_name='Çaplar')),
                ('lengths', models.TextField(blank=True, help_text='Uzunluk değerlerini virgülle ayırarak girin. Örnek: 40mm, 50mm, 60mm', null=True, verbose_name='Uzunluklar')),
                ('measures', models.TextField(blank=True, help_text='Ölçü değerlerini virgülle ayırarak girin. Örnek: 6x70, 8x90', null=True, verbose_name='Ölçüler')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category')),
            ],
        ),
    ]
