# Generated by Django 3.1 on 2020-08-26 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0038_auto_20200821_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghours',
            name='from_hour',
            field=models.TimeField(default='9:00:00'),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='to_hour',
            field=models.TimeField(default='17:00:00'),
        ),
    ]
