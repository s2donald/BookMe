# Generated by Django 3.1.7 on 2021-04-16 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0066_bookings_paymentintent'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='is_off_day',
            field=models.BooleanField(default=False),
        ),
    ]
