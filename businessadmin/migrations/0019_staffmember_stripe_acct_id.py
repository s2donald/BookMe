# Generated by Django 3.1 on 2021-03-16 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessadmin', '0018_auto_20210109_0257'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmember',
            name='stripe_acct_id',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Stripe Account Id'),
        ),
    ]