# Generated by Django 5.1.3 on 2025-01-19 16:24

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_first',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='ilk açıklama metniiii', verbose_name='ilk açıklama metni'),
        ),
    ]
