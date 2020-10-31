# Generated by Django 3.1 on 2020-10-24 05:21

import consumer.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0039_bookings_guest'),
    ]

    operations = [
        migrations.CreateModel(
            name='extraInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=consumer.models.get_booking_folder)),
                ('car_make', models.CharField(blank=True, max_length=30, null=True)),
                ('car_model', models.CharField(blank=True, max_length=30, null=True)),
                ('car_year', models.IntegerField(blank=True, null=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='consumer.bookings')),
            ],
        ),
    ]