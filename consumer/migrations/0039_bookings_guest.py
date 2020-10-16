# Generated by Django 3.1 on 2020-10-16 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0079_auto_20201011_1559'),
        ('consumer', '0038_remove_bookings_guest'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.clients'),
        ),
    ]
