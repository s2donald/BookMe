# Generated by Django 3.1 on 2020-09-25 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_delete_guest'),
        ('business', '0058_remove_company_clients'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='clients',
            field=models.ManyToManyField(related_name='clients', to='account.Clients'),
        ),
    ]
