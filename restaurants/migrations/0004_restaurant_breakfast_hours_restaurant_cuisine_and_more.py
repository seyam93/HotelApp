# Generated by Django 5.1.4 on 2025-04-26 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_restaurant_menu_file_restaurant_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='breakfast_hours',
            field=models.CharField(blank=True, default='Breakfast: 6.00 am – 11.00 am (daily)', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='cuisine',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='dinner_hours',
            field=models.CharField(blank=True, default='Dinner: 6.00 pm – 11.00 pm (daily)', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='dress_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='lunch_hours',
            field=models.CharField(blank=True, default='Lunch: 12.00 pm – 3.00 pm (daily)', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='short_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='opening_hours',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
