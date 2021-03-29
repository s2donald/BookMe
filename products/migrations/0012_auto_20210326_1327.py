# Generated by Django 3.1 on 2021-03-26 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20210325_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addonproducts',
            name='description',
        ),
        migrations.AddField(
            model_name='addonproducts',
            name='is_multiple',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='addonproducts',
            name='is_required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mainproductdropdown',
            name='is_multiple',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mainproductdropdown',
            name='is_required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='productdropdown',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=10),
            preserve_default=False,
        ),
    ]
