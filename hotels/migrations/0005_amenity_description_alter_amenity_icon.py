# Generated by Django 5.1.4 on 2025-04-23 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0004_amenity_room_amenities"),
    ]

    operations = [
        migrations.AddField(
            model_name="amenity",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="amenity",
            name="icon",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
