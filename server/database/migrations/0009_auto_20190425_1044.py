# Generated by Django 2.1.7 on 2019-04-25 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_servicemetadata_db_name_0'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicemetadata',
            name='updated_0',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='servicemetadata',
            name='updated_1',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='servicemetadata',
            name='updated_2',
            field=models.BooleanField(default=True),
        ),
    ]