"""
Data Serializers for AirBnB Backend - Property Rental Platform

Author: Martin Mawien
Copyright (c) 2026 Martin Mawien
GitHub: https://github.com/Martin-Mawien/airbnb-backend

Provides serialization and validation for:
- User profiles with role management
- Property listings with nested images
- Booking validation and conflict detection
- Payment tracking
- Review system with constraints
- Wishlist management
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Property, PropertyImage, Booking, Payment, Review, Wishlist


class UserSerializer(serializers.ModelSerializer):
	"""Serializer for Django User model"""
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'first_name', 'last_name']
		read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
	"""Serializer for user profiles with nested user data"""
	user = UserSerializer(read_only=True)
	username = serializers.CharField(source='user.username', read_only=True)
	
	class Meta:
		model = UserProfile
		fields = ['id', 'user', 'username', 'name', 'email', 'role', 'phone', 'bio', 'avatar', 'created_at']
		read_only_fields = ['id', 'created_at', 'user']


class PropertyImageSerializer(serializers.ModelSerializer):
	"""Serializer for property images"""
	class Meta:
		model = PropertyImage
		fields = ['id', 'property', 'image', 'is_primary', 'created_at']
		read_only_fields = ['id', 'created_at']


class PropertySerializer(serializers.ModelSerializer):
	"""Serializer for properties with nested images and owner info"""
	owner_name = serializers.CharField(source='owner.username', read_only=True)
	images = PropertyImageSerializer(many=True, read_only=True)
	average_rating = serializers.SerializerMethodField()
	review_count = serializers.SerializerMethodField()
	
	class Meta:
		model = Property
		fields = [
			'id', 'owner', 'owner_name', 'title', 'location', 'price', 
			'description', 'status', 'images', 'average_rating', 'review_count'
		]
		read_only_fields = ['id', 'owner']
	
	def get_average_rating(self, obj):
		"""Calculate average rating from reviews"""
		reviews = obj.reviews.all()
		if reviews:
			return round(sum(r.rating for r in reviews) / len(reviews), 1)
		return None
	
	def get_review_count(self, obj):
		"""Get total number of reviews"""
		return obj.reviews.count()
	
	def validate_price(self, value):
		"""Ensure price is positive"""
		if value <= 0:
			raise serializers.ValidationError("Price must be greater than 0")
		return value


class BookingSerializer(serializers.ModelSerializer):
	"""Serializer for bookings with validation"""
	user_name = serializers.CharField(source='user.username', read_only=True)
	property_title = serializers.CharField(source='property.title', read_only=True)
	total_nights = serializers.SerializerMethodField()
	total_price = serializers.SerializerMethodField()
	
	class Meta:
		model = Booking
		fields = [
			'id', 'user', 'user_name', 'property', 'property_title',
			'check_in_date', 'check_out_date', 'status',
			'total_nights', 'total_price'
		]
		read_only_fields = ['id', 'user']
	
	def get_total_nights(self, obj):
		"""Calculate total nights of stay"""
		if obj.check_in_date and obj.check_out_date:
			return (obj.check_out_date - obj.check_in_date).days
		return 0
	
	def get_total_price(self, obj):
		"""Calculate total price based on nights"""
		nights = self.get_total_nights(obj)
		return float(obj.property.price) * nights if nights > 0 else 0
	
	def validate(self, data):
		"""Validate booking dates"""
		check_in = data.get('check_in_date')
		check_out = data.get('check_out_date')
		
		if check_in and check_out:
			if check_out <= check_in:
				raise serializers.ValidationError(
					"Check-out date must be after check-in date"
				)
			
			# Check for overlapping bookings
			property_obj = data.get('property')
			overlapping = Booking.objects.filter(
				property=property_obj,
				status__in=['pending', 'confirmed']
			).filter(
				check_in_date__lt=check_out,
				check_out_date__gt=check_in
			)
			
			# Exclude current booking if updating
			if self.instance:
				overlapping = overlapping.exclude(id=self.instance.id)
			
			if overlapping.exists():
				raise serializers.ValidationError(
					"Property is already booked for these dates"
				)
		
		return data


class PaymentSerializer(serializers.ModelSerializer):
	"""Serializer for payments"""
	booking_details = BookingSerializer(source='booking', read_only=True)
	
	class Meta:
		model = Payment
		fields = ['id', 'booking', 'booking_details', 'amount', 'status', 'payment_date']
		read_only_fields = ['id', 'payment_date']
	
	def validate_amount(self, value):
		"""Ensure amount is positive"""
		if value <= 0:
			raise serializers.ValidationError("Amount must be greater than 0")
		return value


class ReviewSerializer(serializers.ModelSerializer):
	"""Serializer for reviews"""
	user_name = serializers.CharField(source='user.username', read_only=True)
	property_title = serializers.CharField(source='property.title', read_only=True)
	
	class Meta:
		model = Review
		fields = [
			'id', 'user', 'user_name', 'property', 'property_title',
			'booking', 'rating', 'comment'
		]
		read_only_fields = ['id', 'user']
	
	def validate_rating(self, value):
		"""Ensure rating is between 1 and 5"""
		if not (1 <= value <= 5):
			raise serializers.ValidationError("Rating must be between 1 and 5")
		return value
	
	def validate(self, data):
		"""Ensure user has booked the property before reviewing"""
		user = self.context['request'].user
		property_obj = data.get('property')
		booking = data.get('booking')
		
		# Verify booking belongs to user and property
		if booking:
			if booking.user != user:
				raise serializers.ValidationError("You can only review your own bookings")
			if booking.property != property_obj:
				raise serializers.ValidationError("Booking must be for the property being reviewed")
			if booking.status != 'confirmed':
				raise serializers.ValidationError("You can only review confirmed bookings")
		
		# Check if user has already reviewed this property
		if not self.instance:  # Only check on create, not update
			existing_review = Review.objects.filter(
				user=user,
				property=property_obj
			).exists()
			if existing_review:
				raise serializers.ValidationError("You have already reviewed this property")
		
		return data


class WishlistSerializer(serializers.ModelSerializer):
	"""Serializer for wishlists with nested properties"""
	properties = PropertySerializer(many=True, read_only=True)
	property_count = serializers.SerializerMethodField()
	
	class Meta:
		model = Wishlist
		fields = ['id', 'user', 'name', 'properties', 'property_count', 'created_at']
		read_only_fields = ['id', 'user', 'created_at']
	
	def get_property_count(self, obj):
		"""Get total number of properties in wishlist"""
		return obj.properties.count()
