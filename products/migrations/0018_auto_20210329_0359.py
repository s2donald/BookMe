# Generated by Django 3.1.7 on 2021-03-29 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20210329_0056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addonproducts',
            name='mainimage',
        ),
        migrations.RemoveField(
            model_name='addonproducts',
            name='stock',
        ),
    ]
