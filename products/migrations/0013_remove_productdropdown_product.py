# Generated by Django 3.1 on 2021-03-26 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20210326_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productdropdown',
            name='product',
        ),
    ]
