# Generated by Django 3.1 on 2021-01-19 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0055_auto_20210117_0813'),
        ('business', '0099_auto_20210106_2243'),
        ('calendarapp', '0004_auto_20210119_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='formbuilder',
            name='services',
            field=models.ManyToManyField(null=True, related_name='forms_attached', to='business.Services'),
        ),
        migrations.RemoveField(
            model_name='formbuilder',
            name='booking',
        ),
        migrations.AddField(
            model_name='formbuilder',
            name='booking',
            field=models.ManyToManyField(null=True, related_name='booking_form', to='consumer.Bookings'),
        ),
        migrations.AlterField(
            model_name='formbuilder',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_forms', to='business.company'),
        ),
    ]