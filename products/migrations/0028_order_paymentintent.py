# Generated by Django 3.1.7 on 2021-04-17 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_auto_20210416_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paymentintent',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Payment Intent'),
        ),
    ]