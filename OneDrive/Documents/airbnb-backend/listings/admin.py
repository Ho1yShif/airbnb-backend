"""
Django Admin Configuration for AirBnB Backend

Author: Martin Mawien
Copyright (c) 2026 Martin Mawien
GitHub: https://github.com/Martin-Mawien/airbnb-backend

Admin interface customization for all models.
"""

from django.contrib import admin
from .models import UserProfile, Property, PropertyImage, Booking, Payment, Review, Wishlist


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email', 'name', 'email']
    readonly_fields = ['created_at']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'price', 'owner']
    list_filter = ['location']
    search_fields = ['title', 'location']


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['property', 'user', 'check_in_date', 'check_out_date', 'status']
    list_filter = ['status', 'check_in_date', 'check_out_date']
    search_fields = ['property__title', 'user__username']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'status', 'payment_date']
    list_filter = ['status', 'payment_date']
    search_fields = ['booking__property__title', 'booking__user__username']
    readonly_fields = ['payment_date']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['property', 'user', 'rating', 'comment']
    list_filter = ['rating']
    search_fields = ['property__title', 'user__username', 'comment']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'name']
    readonly_fields = ['created_at']
