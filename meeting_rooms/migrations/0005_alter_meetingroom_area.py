# Generated by Django 5.1.4 on 2025-05-03 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_rooms', '0004_alter_meetingroomamenity_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingroom',
            name='area',
            field=models.PositiveIntegerField(blank=True, default=30, help_text='Area in square meters', null=True),
        ),
    ]
