# Generated by Django 3.1 on 2021-03-25 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20210324_1846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productdropdown',
            old_name='name',
            new_name='option',
        ),
    ]
