# Generated by Django 2.1.7 on 2019-03-05 20:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('studying', '0004_auto_20190305_2223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testing',
            name='students',
        ),
        migrations.AlterField(
            model_name='testing',
            name='test_closing_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 5, 20, 36, 27, 334746, tzinfo=utc)),
        ),
    ]
