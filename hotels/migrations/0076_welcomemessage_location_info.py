# Generated by Django 5.1.4 on 2025-05-20 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0075_newslettersubscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='welcomemessage',
            name='location_info',
            field=models.TextField(default='Location information goes here.'),
        ),
    ]
