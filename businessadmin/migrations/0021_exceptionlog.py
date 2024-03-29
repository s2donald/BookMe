# Generated by Django 3.1 on 2021-03-21 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessadmin', '0020_auto_20210316_1219'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExceptionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='Time Stamp')),
                ('view', models.CharField(max_length=30, verbose_name='View')),
                ('exceptionclass', models.CharField(max_length=60, verbose_name='Exception Class')),
                ('message', models.CharField(max_length=100, verbose_name='Exception Message')),
            ],
        ),
    ]
