# Generated by Django 3.1 on 2020-09-25 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20200925_0119'),
        ('business', '0060_auto_20200925_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='clients',
            field=models.ManyToManyField(blank=True, null=True, related_name='clients', to='account.Clients'),
        ),
    ]
