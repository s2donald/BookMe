# Generated by Django 3.1 on 2020-09-28 06:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0069_remove_company_avgrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='companies_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]