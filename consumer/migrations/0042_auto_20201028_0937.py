# Generated by Django 3.1 on 2020-10-28 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0041_auto_20201026_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='review',
            field=models.TextField(max_length=500),
        ),
    ]
