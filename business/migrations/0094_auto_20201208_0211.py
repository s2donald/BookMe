# Generated by Django 3.1 on 2020-12-08 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0093_company_calendarics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenities',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_amenity', to='business.company'),
        ),
    ]