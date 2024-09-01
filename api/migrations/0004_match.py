# Generated by Django 5.0.7 on 2024-07-20 08:21

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_game"),
    ]

    operations = [
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField(auto_created=True, auto_now=True)),
                (
                    "endTime",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 7, 21, 8, 21, 53, 137446)
                    ),
                ),
                (
                    "prize_per_game_play",
                    models.DecimalField(decimal_places=2, default=0.05, max_digits=5),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.game"
                    ),
                ),
            ],
        ),
    ]
