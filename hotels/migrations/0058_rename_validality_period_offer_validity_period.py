# Generated by Django 5.1.4 on 2025-05-02 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0057_offer_offer_code_offer_terms_and_conditions_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='validality_period',
            new_name='validity_period',
        ),
    ]
