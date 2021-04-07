# Generated by Django 3.1 on 2021-03-03 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0111_remove_companyreq_approved'),
        ('consumer', '0063_remove_bookings_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='bookingreq',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking_request', to='business.companyreq'),
        ),
    ]