# Generated by Django 3.1.7 on 2021-04-28 02:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0052_auto_20210427_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='dateshipped',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
