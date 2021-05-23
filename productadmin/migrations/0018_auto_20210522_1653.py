# Generated by Django 3.1.7 on 2021-05-22 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productadmin', '0017_auto_20210522_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricebasedshippingrate',
            name='names',
            field=models.CharField(default='s', max_length=200, verbose_name=''),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='pricebasedshippingrate',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='pricebasedshippingrate',
            name='name',
        ),
    ]
