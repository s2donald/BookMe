# Generated by Django 3.1.7 on 2021-05-20 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0120_auto_20210415_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='background',
            field=models.CharField(choices=[('primary', 'primary'), ('carbon', 'carbon'), ('hexagon', 'hexagon')], default='carbon', max_length=200),
        ),
    ]
