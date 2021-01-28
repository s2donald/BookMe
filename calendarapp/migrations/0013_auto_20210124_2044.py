# Generated by Django 3.1 on 2021-01-25 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0012_auto_20210119_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingform',
            name='label',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formbuilder',
            name='is_checkbox',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No')], default='n', max_length=3),
        ),
        migrations.AlterField(
            model_name='formbuilder',
            name='is_integer',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No')], default='n', max_length=3),
        ),
        migrations.AlterField(
            model_name='formbuilder',
            name='is_required',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No')], default='n', max_length=3),
        ),
        migrations.AlterField(
            model_name='formbuilder',
            name='is_text',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No')], default='y', max_length=3),
        ),
    ]
