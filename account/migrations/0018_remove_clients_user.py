# Generated by Django 3.1 on 2020-09-25 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20200925_0100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clients',
            name='user',
        ),
    ]