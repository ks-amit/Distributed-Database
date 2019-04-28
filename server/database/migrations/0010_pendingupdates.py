# Generated by Django 2.1.7 on 2019-04-26 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20190425_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingUpdates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=3000)),
                ('addr', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('POST', 'POST'), ('GET', 'GET'), ('PUT', 'PUT')], max_length=4)),
            ],
        ),
    ]