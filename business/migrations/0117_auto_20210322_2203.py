# Generated by Django 3.1 on 2021-03-23 02:03

import business.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0116_auto_20210319_0343'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='backgroundimage',
            field=models.ImageField(blank=True, upload_to=business.models.get_user_backgroundimage_folder),
        ),
        migrations.AddField(
            model_name='company',
            name='business_type',
            field=models.CharField(choices=[('product', 'Product Verticle'), ('service', 'Services Verticle')], default='product', max_length=60),
        ),
        migrations.AlterField(
            model_name='company',
            name='interval',
            field=models.IntegerField(choices=[(5, '5 Minutes'), (10, '10 Minutes'), (15, '15 Minutes'), (20, '20 Minutes'), (25, '25 Minutes'), (30, '30 Minutes'), (35, '35 Minutes'), (40, '40 Minutes'), (45, '45 Minutes'), (50, '50 Minutes'), (55, '55 Minutes'), (60, '60 Minutes')], default=30),
        ),
    ]
