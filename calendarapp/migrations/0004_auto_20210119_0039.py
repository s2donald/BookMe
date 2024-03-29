# Generated by Django 3.1 on 2021-01-19 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0099_auto_20210106_2243'),
        ('consumer', '0055_auto_20210117_0813'),
        ('calendarapp', '0003_auto_20210105_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='formbuilder',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_booking_form', to='business.company'),
        ),
        migrations.AlterField(
            model_name='formbuilder',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_form', to='consumer.bookings'),
        ),
    ]
