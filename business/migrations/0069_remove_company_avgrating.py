# Generated by Django 3.1 on 2020-09-27 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0068_auto_20200926_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='avgrating',
        ),
    ]
