# Generated by Django 3.1.7 on 2021-05-22 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productadmin', '0006_delete_shippingzone'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CompanyShippingZone',
        ),
    ]
