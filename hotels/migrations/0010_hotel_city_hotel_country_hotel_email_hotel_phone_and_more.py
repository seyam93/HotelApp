# Generated by Django 5.1.4 on 2025-04-23 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0009_alter_feature_icon_alter_offer_discount_percentage_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="hotel",
            name="city",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="hotel",
            name="country",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="hotel",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="hotel",
            name="phone",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="hotel",
            name="star_rating",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "1 Star"),
                    (2, "2 Star"),
                    (3, "3 Star"),
                    (4, "4 Star"),
                    (5, "5 Star"),
                ],
                default=1,
            ),
        ),
        migrations.AddField(
            model_name="hotel",
            name="title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="hotelservice",
            name="hotel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hotel_services",
                to="hotels.hotel",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="hotel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="hotels.hotel",
            ),
        ),
    ]
