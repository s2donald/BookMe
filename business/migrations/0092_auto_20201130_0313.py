# Generated by Django 3.1 on 2020-11-30 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0091_auto_20201128_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='darkmode',
            field=models.BooleanField(default=True),
        ),
    ]