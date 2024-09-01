# Generated by Django 5.0.7 on 2024-09-01 02:53

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0013_coupon_alter_match_end_time_alter_match_start_time"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="end_time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 9, 2, 8, 38, 31, 269946)
            ),
        ),
        migrations.AlterField(
            model_name="match",
            name="start_time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 9, 1, 8, 38, 31, 269937)
            ),
        ),
        migrations.CreateModel(
            name="WithdrawlRequest",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "coupon",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.coupon",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
