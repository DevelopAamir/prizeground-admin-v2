# Generated by Django 5.0.7 on 2024-07-20 08:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_match_credentials_alter_match_end_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="end_time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 21, 14, 39, 0, 961461)
            ),
        ),
        migrations.AlterField(
            model_name="match",
            name="start_time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 20, 14, 39, 0, 961452)
            ),
        ),
    ]
