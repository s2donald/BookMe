# Generated by Django 3.1.7 on 2021-04-24 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0045_questionmodels_placeholder'),
    ]

    operations = [
        migrations.AddField(
            model_name='answermodels',
            name='orderitem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answer_orderitems', to='products.orderitem'),
            preserve_default=False,
        ),
    ]
