# Generated by Django 3.1.7 on 2021-04-17 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0120_auto_20210415_1334'),
        ('products', '0028_order_paymentintent'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('business', 'slug')},
        ),
    ]