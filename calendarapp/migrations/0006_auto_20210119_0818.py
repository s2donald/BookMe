# Generated by Django 3.1 on 2021-01-19 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0055_auto_20210117_0813'),
        ('business', '0099_auto_20210106_2243'),
        ('calendarapp', '0005_auto_20210119_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formbuilder',
            name='booking',
            field=models.ManyToManyField(related_name='booking_form', to='consumer.Bookings'),
        ),
        migrations.AlterField(
            model_name='formbuilder',
            name='services',
            field=models.ManyToManyField(related_name='forms_attached', to='business.Services'),
        ),
    ]