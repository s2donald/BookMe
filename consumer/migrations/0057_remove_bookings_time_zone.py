# Generated by Django 3.1 on 2021-02-17 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0056_bookings_time_zone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='time_zone',
        ),
    ]