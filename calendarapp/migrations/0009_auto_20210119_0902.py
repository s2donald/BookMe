# Generated by Django 3.1 on 2021-01-19 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0099_auto_20210106_2243'),
        ('calendarapp', '0008_auto_20210119_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formbuilder',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_forms', to='business.company'),
        ),
        migrations.AlterField(
            model_name='formbuilder',
            name='integer',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formbuilder',
            name='text',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
