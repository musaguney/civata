# Generated by Django 5.1.3 on 2025-01-19 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_description_first'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='coating',
            field=models.CharField(choices=[('Yok', 'Yok'), ('Var (Zn Cr⁺³)', 'Var (Zn Cr⁺³)')], max_length=20, verbose_name='Kaplama'),
        ),
    ]
