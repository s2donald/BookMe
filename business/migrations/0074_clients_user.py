# Generated by Django 3.1 on 2020-10-10 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0073_company_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_booked', to=settings.AUTH_USER_MODEL),
        ),
    ]
