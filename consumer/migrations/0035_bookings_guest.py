# Generated by Django 3.1 on 2020-09-25 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_auto_20200925_1402'),
        ('consumer', '0034_auto_20200925_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.clients'),
        ),
    ]
