# Generated by Django 3.1 on 2021-03-23 03:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gallaryproductimage',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='gallaryproductimage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]