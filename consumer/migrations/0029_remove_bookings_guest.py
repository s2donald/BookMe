# Generated by Django 3.1 on 2020-09-25 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0028_auto_20200925_0924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='guest',
        ),
    ]