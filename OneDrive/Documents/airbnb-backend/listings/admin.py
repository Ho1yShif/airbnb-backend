from django.contrib import admin
from .models import UserProfile, Property, PropertyImage, Booking, Payment, Review, Wishlist, Address, CustomerPreferences


@admin.register(UserProfile)
class ProfileAdministration(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'contact_email', 'user_role', 'registration_date']
    list_filter = ['user_role', 'registration_date']
    search_fields = ['user__username', 'user__email', 'full_name', 'contact_email']
    readonly_fields = ['registration_date']


@admin.register(Property)
class ListingAdministration(admin.ModelAdmin):
    list_display = ['listing_title', 'property_location', 'nightly_rate', 'property_owner']
    list_filter = ['property_location']
    search_fields = ['listing_title', 'property_location']


@admin.register(PropertyImage)
class PhotoAdministration(admin.ModelAdmin):
    list_display = ['listing', 'set_as_primary', 'uploaded_at']
    list_filter = ['set_as_primary', 'uploaded_at']


@admin.register(Booking)
class ReservationAdministration(admin.ModelAdmin):
    list_display = ['reserved_property', 'guest', 'arrival_date', 'departure_date', 'reservation_state']
    list_filter = ['reservation_state', 'arrival_date', 'departure_date']
    search_fields = ['reserved_property__listing_title', 'guest__username']


@admin.register(Payment)
class TransactionAdministration(admin.ModelAdmin):
    list_display = ['reservation', 'transaction_amount', 'payment_state', 'processed_at']
    list_filter = ['payment_state', 'processed_at']
    search_fields = ['reservation__reserved_property__listing_title', 'reservation__guest__username']
    readonly_fields = ['processed_at']


@admin.register(Review)
class FeedbackAdministration(admin.ModelAdmin):
    list_display = ['reviewed_property', 'reviewer', 'rating_score', 'review_text']
    list_filter = ['rating_score']
    search_fields = ['reviewed_property__listing_title', 'reviewer__username', 'review_text']


@admin.register(Wishlist)
class SavedItemsAdministration(admin.ModelAdmin):
    list_display = ['owner', 'list_name', 'created_on']
    list_filter = ['created_on']
    search_fields = ['owner__username', 'list_name']
    readonly_fields = ['created_on']


@admin.register(Address)
class LocationAdministration(admin.ModelAdmin):
    list_display = ['account_owner', 'address_category', 'city_name', 'state_province', 'country_name', 'primary_address']
    list_filter = ['address_category', 'country_name', 'primary_address']
    search_fields = ['account_owner__username', 'city_name', 'state_province', 'street_line']


@admin.register(CustomerPreferences)
class PreferenceAdministration(admin.ModelAdmin):
    list_display = ['account', 'enable_email_alerts', 'enable_sms_alerts', 'subscribe_newsletter']
    list_filter = ['enable_email_alerts', 'enable_sms_alerts', 'subscribe_newsletter']
    search_fields = ['account__username']
