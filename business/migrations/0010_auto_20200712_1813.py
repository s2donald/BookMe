# Generated by Django 3.0.1 on 2020-07-12 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_auto_20200711_0400'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='company',
            index_together={('slug', 'id')},
        ),
    ]
