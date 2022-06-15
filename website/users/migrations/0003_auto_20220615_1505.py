# Generated by Django 3.2 on 2022-06-15 13:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_auto_20220615_1504"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="date_joined",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 6, 15, 13, 5, 1, 912679, tzinfo=utc)
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="previous_user_tier",
            field=models.CharField(max_length=1000, verbose_name=1270714854816),
        ),
    ]
