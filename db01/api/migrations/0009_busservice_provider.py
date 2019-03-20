# Generated by Django 2.1.7 on 2019-03-19 22:37

import api.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190318_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='busservice',
            name='provider',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=api.models.BusService.default_array_field, size=None),
        ),
    ]