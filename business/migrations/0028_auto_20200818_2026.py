# Generated by Django 3.0.1 on 2020-08-19 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0027_auto_20200817_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
