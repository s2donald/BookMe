# Generated by Django 3.1 on 2021-01-08 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('businessadmin', '0016_staffmember_pfp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffmember',
            old_name='pfp',
            new_name='image',
        ),
    ]
