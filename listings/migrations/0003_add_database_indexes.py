"""
Database migration to add indexes for query optimization.

Run with: python manage.py migrate
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_rename_property_fields'),
    ]

    operations = [
        # Property indexes
        migrations.AddIndex(
            model_name='property',
            index=models.Index(
                fields=['property_owner', 'listing_status'],
                name='property_owner_status_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(
                fields=['listing_status', 'nightly_rate'],
                name='status_rate_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(
                fields=['listed_on'],
                name='property_listed_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(
                fields=['property_location'],
                name='property_location_idx',
            ),
        ),
        
        # Booking indexes
        migrations.AddIndex(
            model_name='booking',
            index=models.Index(
                fields=['guest', 'reservation_state'],
                name='booking_guest_state_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='booking',
            index=models.Index(
                fields=['reserved_property', 'reservation_state'],
                name='booking_property_state_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='booking',
            index=models.Index(
                fields=['arrival_date', 'departure_date'],
                name='booking_dates_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='booking',
            index=models.Index(
                fields=['created_at'],
                name='booking_created_idx',
            ),
        ),
        
        # Review indexes
        migrations.AddIndex(
            model_name='review',
            index=models.Index(
                fields=['reviewed_property', 'rating'],
                name='review_property_rating_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(
                fields=['reviewer'],
                name='review_reviewer_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(
                fields=['posted_on'],
                name='review_posted_idx',
            ),
        ),
        
        # Wishlist indexes
        migrations.AddIndex(
            model_name='wishlist',
            index=models.Index(
                fields=['user', 'property'],
                name='wishlist_user_property_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='wishlist',
            index=models.Index(
                fields=['added_date'],
                name='wishlist_added_idx',
            ),
        ),
        
        # User profile indexes
        migrations.AddIndex(
            model_name='userprofile',
            index=models.Index(
                fields=['user_role'],
                name='userprofile_role_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='userprofile',
            index=models.Index(
                fields=['registration_date'],
                name='userprofile_registered_idx',
            ),
        ),
    ]
