# Generated by Django 3.1 on 2020-09-22 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0056_auto_20200922_0253'),
        ('consumer', '0021_auto_20200914_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_reviews', to='business.company'),
        ),
    ]