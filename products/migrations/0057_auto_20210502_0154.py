# Generated by Django 3.1.7 on 2021-05-02 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0056_auto_20210502_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answermodels',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
