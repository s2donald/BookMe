# Generated by Django 3.1.7 on 2021-04-16 21:51

import address.models
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_auto_20200830_1851'),
        ('products', '0021_remove_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.address'),
        ),
    ]
