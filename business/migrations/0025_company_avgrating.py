# Generated by Django 3.0.1 on 2020-08-16 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0024_company_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='avgrating',
            field=models.DecimalField(decimal_places=2, default=3.5, max_digits=5),
            preserve_default=False,
        ),
    ]