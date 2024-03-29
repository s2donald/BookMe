# Generated by Django 3.1 on 2021-03-23 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_addonproducts_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addonproducts',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
