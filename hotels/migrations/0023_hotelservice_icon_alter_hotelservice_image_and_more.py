# Generated by Django 5.1.4 on 2025-04-24 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0022_review_email_review_profile_picture_review_view_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="hotelservice",
            name="icon",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="hotelservice",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="hotel_services/"),
        ),
        migrations.AlterField(
            model_name="hotelservice",
            name="price",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name="hotelservice",
            name="pricing_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("per_night", "Per Night"),
                    ("daily", "Daily"),
                    ("once", "One Time"),
                ],
                default="per_night",
                max_length=20,
            ),
        ),
    ]
