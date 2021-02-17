# Generated by Django 3.1 on 2021-02-17 01:42

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0101_company_background'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='tz',
            field=timezone_field.fields.TimeZoneField(default='America/Toronto'),
        ),
    ]
