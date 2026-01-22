# Generated migration to rename Property model fields

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='owner',
            new_name='property_owner',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='title',
            new_name='listing_title',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='location',
            new_name='property_location',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='price',
            new_name='nightly_rate',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='description',
            new_name='property_description',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='status',
            new_name='listing_status',
        ),
    ]
