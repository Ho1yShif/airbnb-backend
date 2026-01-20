"""
Property rental platform database schema.

Implements core rental marketplace functionality including user management,
property listings, reservation system, payment processing, and user reviews.
"""

from decimal import Decimal
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    USER_ROLES = (
        ('guest', 'Guest'),
        ('host', 'Property Owner'),
        ('admin', 'Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True)
    contact_email = models.EmailField(blank=True)
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default='guest')
    phone_number = models.CharField(max_length=20, blank=True)
    biography = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='user_avatars/', blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_user_role_display()})"
    
    def is_property_owner(self):
        return self.user_role == 'host'
    
    class Meta:
        ordering = ['-registration_date']
        db_table = 'user_profiles'


@receiver(post_save, sender=User)
def auto_generate_profile_instance(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            full_name=f"{instance.first_name} {instance.last_name}".strip() or instance.username,
            contact_email=instance.email
        )
    else:
        try:
            instance.profile.save(update_fields=['biography', 'phone_number'])
        except UserProfile.DoesNotExist:
            pass


class Property(models.Model):
    AVAILABILITY_STATUS = (
        ('available', 'Ready to Book'),
        ('unavailable', 'Not Available'),
        ('under_review', 'Under Review'),
    )

    property_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties')
    listing_title = models.CharField(max_length=200)
    property_location = models.CharField(max_length=300)
    nightly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    property_description = models.TextField(blank=True)
    listing_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='available')
    listed_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.listing_title} - {self.property_location}"
    
    def calculate_booking_cost(self, num_nights):
        return self.nightly_rate * num_nights
    
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-listed_on']
        db_table = 'property_listings'


class PropertyImage(models.Model):
    listing = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(upload_to='listing_photos/')
    set_as_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        primary_text = "Primary" if self.set_as_primary else "Secondary"
        return f"{primary_text} photo for {self.listing.listing_title}"
    
    class Meta:
        ordering = ['-set_as_primary', '-uploaded_at']
        db_table = 'listing_photos'
    
    def save(self, *args, **kwargs):
        if self.set_as_primary:
            existing_primary = PropertyImage.objects.filter(
                listing=self.listing, 
                set_as_primary=True
            ).exclude(pk=self.pk)
            
            if existing_primary.exists():
                existing_primary.update(set_as_primary=False)
        elif not PropertyImage.objects.filter(listing=self.listing, set_as_primary=True).exists():
            self.set_as_primary = True
        
        super().save(*args, **kwargs)


class Booking(models.Model):
    RESERVATION_STATES = (
        ('awaiting_approval', 'Awaiting Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    reserved_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reservations')
    arrival_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    reservation_state = models.CharField(max_length=25, choices=RESERVATION_STATES, default='awaiting_approval')
    booked_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.guest.username}'s reservation at {self.reserved_property.listing_title}"
    
    class Meta:
        ordering = ['-booked_on']
        db_table = 'property_reservations'
    
    def clean(self):
        if self.departure_date and self.arrival_date:
            if self.departure_date <= self.arrival_date:
                raise ValidationError({
                    'departure_date': 'Check-out must be scheduled after check-in date'
                })
            
            if self.arrival_date < date.today():
                raise ValidationError({
                    'arrival_date': 'Reservation dates cannot be in the past'
                })
            
            duration = (self.departure_date - self.arrival_date).days
            if duration > 365:
                raise ValidationError({
                    'departure_date': 'Maximum reservation duration is 365 nights'
                })
            
            overlapping = Booking.objects.filter(
                reserved_property=self.reserved_property,
                reservation_state__in=['awaiting_approval', 'approved']
            ).exclude(pk=self.pk)
            
            for existing_reservation in overlapping:
                if not (self.departure_date <= existing_reservation.arrival_date or 
                        self.arrival_date >= existing_reservation.departure_date):
                    raise ValidationError({
                        'arrival_date': 'Selected dates conflict with existing reservation'
                    })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def duration_nights(self):
        if self.arrival_date and self.departure_date:
            return (self.departure_date - self.arrival_date).days
        return 0
    
    @property
    def computed_total_cost(self):
        return self.reserved_property.calculate_booking_cost(self.duration_nights)


class Payment(models.Model):
    TRANSACTION_STATES = (
        ('processing', 'Processing'),
        ('successful', 'Successful'),
        ('declined', 'Declined'),
        ('refunded', 'Refunded'),
    )

    reservation = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='transaction')
    transaction_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_state = models.CharField(max_length=20, choices=TRANSACTION_STATES, default='processing')
    processed_at = models.DateTimeField(auto_now_add=True)
    reference_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Transaction #{self.reference_code or self.id} - {self.get_payment_state_display()}"

    class Meta:
        ordering = ['-processed_at']
        db_table = 'payment_transactions'


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_reviews')
    reviewed_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_reviews')
    associated_booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='review_entry', null=True, blank=True)
    rating_score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reviewer.username}'s {self.rating_score}-star review"
    
    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['reviewer', 'associated_booking']
        db_table = 'property_reviews'


class Wishlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_lists')
    list_name = models.CharField(max_length=100)
    saved_properties = models.ManyToManyField(Property, related_name='favorited_by', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username}'s '{self.list_name}' collection"
    
    @property
    def item_count(self):
        return self.saved_properties.count()

    class Meta:
        ordering = ['-created_on']
        db_table = 'user_wishlists'


class Address(models.Model):
    ADDRESS_TYPES = (
        ('billing', 'Billing Address'),
        ('shipping', 'Delivery Address'),
    )
    
    account_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stored_addresses')
    address_category = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='billing')
    street_line = models.CharField(max_length=255)
    city_name = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country_name = models.CharField(max_length=100)
    primary_address = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_address_category_display()} - {self.city_name}, {self.state_province}"

    class Meta:
        ordering = ['-primary_address', '-added_on']
        verbose_name_plural = "Addresses"
        db_table = 'customer_addresses'


class CustomerPreferences(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_preferences')
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    favorite_destinations = models.TextField(blank=True, help_text="Comma-delimited location preferences")
    desired_amenities = models.TextField(blank=True, help_text="Comma-delimited amenity preferences")
    enable_email_alerts = models.BooleanField(default=True)
    enable_sms_alerts = models.BooleanField(default=False)
    subscribe_newsletter = models.BooleanField(default=True)
    preference_set_on = models.DateTimeField(auto_now_add=True)
    preference_updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.account.username}"

    class Meta:
        verbose_name_plural = "Customer Preferences"
        db_table = 'user_preferences'