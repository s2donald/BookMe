# Generated by Django 3.1.7 on 2021-06-08 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0031_auto_20210310_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='rates',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)], default=1),
            preserve_default=False,
        ),
    ]