# Generated by Django 3.1 on 2020-08-20 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0031_openinghours'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='interval',
            field=models.IntegerField(choices=[(5, '5 Minutes'), (10, '10 Minutes')], default=1),
        ),
    ]