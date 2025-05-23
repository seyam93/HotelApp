# Generated by Django 5.1.4 on 2025-05-02 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0056_alter_hotelservice_pricing_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='offer_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='terms_and_conditions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='validality_period',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
