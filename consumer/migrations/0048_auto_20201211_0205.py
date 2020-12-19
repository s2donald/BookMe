# Generated by Django 3.1 on 2020-12-11 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0095_auto_20201210_0217'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consumer', '0047_auto_20201203_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.clients'),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
