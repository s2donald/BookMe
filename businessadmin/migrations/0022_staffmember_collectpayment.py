# Generated by Django 3.1.7 on 2021-03-30 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessadmin', '0021_exceptionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmember',
            name='collectpayment',
            field=models.BooleanField(default=False),
        ),
    ]
