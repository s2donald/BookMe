# Generated by Django 3.0.1 on 2020-07-09 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_company_users'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='users',
            new_name='user',
        ),
    ]
