# Generated by Django 3.1 on 2020-12-31 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessadmin', '0014_auto_20201229_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breaks',
            name='to_hour',
            field=models.TimeField(default='13:00 PM'),
        ),
        migrations.AlterField(
            model_name='staffworkinghours',
            name='from_hour',
            field=models.TimeField(default='9:00 AM'),
        ),
        migrations.AlterField(
            model_name='staffworkinghours',
            name='to_hour',
            field=models.TimeField(default='5:00 PM'),
        ),
    ]
