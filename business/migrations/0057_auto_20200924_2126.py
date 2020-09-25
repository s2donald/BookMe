# Generated by Django 3.1 on 2020-09-25 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_clients'),
        ('business', '0056_auto_20200922_0253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='guest_client',
        ),
        migrations.AlterField(
            model_name='company',
            name='clients',
            field=models.ManyToManyField(related_name='clients', to='account.Clients'),
        ),
    ]
