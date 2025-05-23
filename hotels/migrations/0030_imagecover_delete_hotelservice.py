# Generated by Django 5.1.4 on 2025-04-25 00:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0029_sociallink"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImageCover",
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
                ("image", models.ImageField(upload_to="image_covers/")),
                ("caption", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "hotel",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="image_covers",
                        to="hotels.hotel",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="image_covers",
                        to="hotels.room",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="HotelService",
        ),
    ]
