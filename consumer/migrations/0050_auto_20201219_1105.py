# Generated by Django 3.1 on 2020-12-19 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0049_bookings_staffmem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookings',
            options={'ordering': ('-start',), 'verbose_name': 'booking', 'verbose_name_plural': 'bookings'},
        ),
    ]