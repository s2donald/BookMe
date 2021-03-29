# Generated by Django 3.1 on 2021-03-27 03:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0118_auto_20210322_2355'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consumer', '0064_auto_20210303_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.clients'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='reviewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
