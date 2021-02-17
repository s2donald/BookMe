# Generated by Django 3.1 on 2021-02-17 01:54

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0055_auto_20210117_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='time_zone',
            field=timezone_field.fields.TimeZoneField(default='America/Toronto'),
        ),
    ]