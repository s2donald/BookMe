# Generated by Django 3.1.7 on 2021-06-13 04:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0126_company_referedby'),
        ('products', '0063_orderitem_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('active', models.BooleanField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupon_code', to='business.company')),
            ],
            options={
                'unique_together': {('company', 'code')},
            },
        ),
    ]
