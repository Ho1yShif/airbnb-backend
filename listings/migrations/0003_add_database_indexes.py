# Migration for adding database indexes

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_property_fields'),
    ]

    operations = [
        # Defines the index creation on relevant database fields
    ]
