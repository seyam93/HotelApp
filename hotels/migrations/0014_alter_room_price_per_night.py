# Generated by Django 5.1.4 on 2025-04-24 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0013_room_number_of_bathrooms_room_room_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='price_per_night',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8),
        ),
    ]
