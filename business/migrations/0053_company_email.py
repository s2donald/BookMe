# Generated by Django 3.1 on 2020-09-19 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0052_remove_company_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(default='sdoll@gibele.com', max_length=60, verbose_name='Business Email'),
        ),
    ]
