# Generated by Django 3.1 on 2020-09-25 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_auto_20200925_1402'),
        ('business', '0064_remove_company_clients'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='clients',
            field=models.ManyToManyField(related_name='clients', to='account.Clients'),
        ),
    ]