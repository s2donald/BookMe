# Generated by Django 3.1 on 2020-12-10 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessadmin', '0006_auto_20201210_0306'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmember',
            name='is_owner',
            field=models.BooleanField(default=False),
        ),
    ]
