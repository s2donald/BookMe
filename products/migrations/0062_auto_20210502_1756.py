# Generated by Django 3.1.7 on 2021-05-02 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0061_auto_20210502_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionmodels',
            name='retrievetype',
            field=models.IntegerField(choices=[(0, 'Free text'), (1, 'Image Attachment')], default=0, verbose_name='Get it in a form of:'),
        ),
    ]
