# Generated by Django 3.1.7 on 2021-05-06 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0120_auto_20210415_1334'),
        ('consumer', '0067_bookings_is_off_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddOnServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='name')),
                ('duration_hour', models.IntegerField(choices=[(0, '0 Hours'), (1, '1 Hour'), (2, '2 Hours'), (3, '3 Hours'), (4, '4 Hours'), (5, '5 Hours'), (6, '6 Hours'), (7, '7 Hours'), (8, '8 Hours'), (9, '9 Hours'), (10, '10 Hours'), (11, '11 Hours'), (12, '12 Hours'), (13, '13 Hours'), (14, '14 Hours'), (15, '15 Hours'), (16, '16 Hours'), (17, '17 Hours'), (18, '18 Hours'), (19, '19 Hours'), (20, '20 Hours'), (21, '21 Hours'), (22, '22 Hours'), (23, '23 Hours')], default=0)),
                ('duration_minute', models.IntegerField(choices=[(0, '0 Minutes'), (5, '5 Minutes'), (10, '10 Minutes'), (15, '15 Minutes'), (20, '20 Minutes'), (25, '25 Minutes'), (30, '30 Minutes'), (35, '35 Minutes'), (40, '40 Minutes'), (45, '45 Minutes'), (50, '50 Minutes'), (55, '55 Minutes')], default=30)),
                ('services', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addon_offered', to='business.services')),
            ],
            options={
                'verbose_name': 'Add On Service',
                'verbose_name_plural': 'Add On Services',
                'ordering': ('-name',),
            },
        ),
    ]