# Generated by Django 3.1 on 2021-01-04 22:14

import businessadmin.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessadmin', '0015_auto_20201231_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmember',
            name='pfp',
            field=models.ImageField(blank=True, upload_to=businessadmin.models.get_staff_image_folder),
        ),
    ]
