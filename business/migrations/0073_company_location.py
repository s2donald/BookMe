# Generated by Django 3.1 on 2020-10-08 03:39

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0072_company_shownotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]