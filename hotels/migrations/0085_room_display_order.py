# Generated by Django 5.1.4 on 2025-06-02 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0084_alter_hotelvideobanner_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='display_order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
