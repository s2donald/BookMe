# Generated by Django 3.1.7 on 2021-03-30 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessadmin', '0024_staffmember_nrfpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmember',
            name='collectnrfpayment',
            field=models.BooleanField(default=False),
        ),
    ]
