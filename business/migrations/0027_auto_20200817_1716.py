# Generated by Django 3.0.1 on 2020-08-17 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0026_amenities'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amenities',
            options={'verbose_name': 'Amenity', 'verbose_name_plural': 'Amenities'},
        ),
    ]