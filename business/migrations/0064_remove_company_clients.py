# Generated by Django 3.1 on 2020-09-25 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0063_auto_20200925_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='clients',
        ),
    ]