# Generated by Django 3.1.7 on 2021-04-20 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0120_auto_20210415_1334'),
        ('products', '0034_auto_20210418_0103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='productcategory',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='business.company'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='services',
            field=models.ManyToManyField(blank=True, to='products.Product'),
        ),
    ]
