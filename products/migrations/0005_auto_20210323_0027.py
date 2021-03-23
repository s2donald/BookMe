# Generated by Django 3.1 on 2021-03-23 04:27

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20210323_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addonproducts',
            name='mainimage',
            field=models.ImageField(blank=True, upload_to=products.models.get_addon_image_folder),
        ),
        migrations.AlterField(
            model_name='product',
            name='mainimage',
            field=models.ImageField(blank=True, upload_to=products.models.get_product_image_folder),
        ),
    ]
