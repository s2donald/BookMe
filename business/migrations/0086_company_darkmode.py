# Generated by Django 3.1 on 2020-11-16 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0085_auto_20201111_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='darkmode',
            field=models.BooleanField(default=False),
        ),
    ]