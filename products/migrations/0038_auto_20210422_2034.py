# Generated by Django 3.1.7 on 2021-04-23 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_auto_20210420_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainproductdropdown',
            name='sublabel',
            field=models.CharField(default='Add Ons:', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Base Price'),
        ),
    ]