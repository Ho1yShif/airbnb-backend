from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import date
from .models import UserProfile, Property, PropertyImage, Booking, Payment, Review, Wishlist, Address, CustomerPreferences


class EmailNotificationSerializer(serializers.Serializer):
	subject = serializers.CharField(max_length=255)
	message = serializers.CharField()
	recipient = serializers.EmailField()


class AccountDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'first_name', 'last_name']
		read_only_fields = ['id']


# Alias for auth_views compatibility
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
		read_only_fields = ['id', 'date_joined']


class ProfileDataSerializer(serializers.ModelSerializer):
	account_info = AccountDataSerializer(source='user', read_only=True)
	account_username = serializers.CharField(source='user.username', read_only=True)
	
	class Meta:
		model = UserProfile
		fields = ['id', 'user', 'account_username', 'account_info', 'full_name', 'contact_email', 'user_role', 'phone_number', 'biography', 'profile_picture', 'registration_date']
		read_only_fields = ['id', 'registration_date', 'user']


class ListingPhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model = PropertyImage
		fields = ['id', 'listing', 'photo', 'set_as_primary', 'uploaded_at']
		read_only_fields = ['id', 'uploaded_at']


class ListingDataSerializer(serializers.ModelSerializer):
	owner_username = serializers.CharField(source='property_owner.username', read_only=True)
	attached_photos = ListingPhotoSerializer(many=True, read_only=True)
	computed_average_score = serializers.SerializerMethodField()
	feedback_total = serializers.SerializerMethodField()
	
	class Meta:
		model = Property
		fields = [
			'id', 'property_owner', 'owner_username', 'listing_title', 'property_location', 'nightly_rate',
			'property_description', 'listing_status', 'attached_photos', 'computed_average_score', 'feedback_total'
		]
		read_only_fields = ['id', 'property_owner']
	
	def get_computed_average_score(self, obj):
		feedback_items = obj.reviews.all()
		if feedback_items:
			score_sum = sum(item.rating_score for item in feedback_items)
			return round(score_sum / len(feedback_items), 1)
		return None
	
	def get_feedback_total(self, obj):
		return obj.reviews.count()
	
	def validate_nightly_rate(self, value):
		if value <= 0:
			raise serializers.ValidationError("Nightly rate must be a positive value")
		return value


class ReservationDataSerializer(serializers.ModelSerializer):
	guest_username = serializers.CharField(source='guest.username', read_only=True)
	property_name = serializers.CharField(source='reserved_property.listing_title', read_only=True)
	stay_duration_nights = serializers.SerializerMethodField()
	computed_cost = serializers.SerializerMethodField()
	
	class Meta:
		model = Booking
		fields = [
			'id', 'guest', 'guest_username', 'reserved_property', 'property_name',
			'arrival_date', 'departure_date', 'reservation_state',
			'stay_duration_nights', 'computed_cost'
		]
		read_only_fields = ['id', 'guest']
	
	def get_stay_duration_nights(self, obj):
		if obj.arrival_date and obj.departure_date:
			return (obj.departure_date - obj.arrival_date).days
		return 0
	
	def get_computed_cost(self, obj):
		nights = self.get_stay_duration_nights(obj)
		return float(obj.reserved_property.nightly_rate) * nights if nights > 0 else 0
	
	def validate(self, data):
		arrival = data.get('arrival_date')
		departure = data.get('departure_date')
		
		if arrival and departure:
			if departure <= arrival:
				raise serializers.ValidationError({
					'departure_date': 'Check-out must be later than check-in'
				})
			
			night_count = (departure - arrival).days
			if night_count < 1:
				raise serializers.ValidationError({
					'arrival_date': 'Minimum stay is one night'
				})
			
			if night_count > 365:
				raise serializers.ValidationError({
					'departure_date': 'Stays exceeding 365 nights not permitted'
				})
			
			property_target = data.get('reserved_property')
			if property_target and property_target.listing_status != 'available':
				raise serializers.ValidationError({
					'reserved_property': 'Selected property is not available for booking'
				})
			
			overlap_query = Booking.objects.filter(
				reserved_property=property_target,
				reservation_state__in=['awaiting_approval', 'approved']
			)
			
			if self.instance:
				overlap_query = overlap_query.exclude(pk=self.instance.pk)
			
			for existing_booking in overlap_query:
				if not (departure <= existing_booking.arrival_date or 
						arrival >= existing_booking.departure_date):
					raise serializers.ValidationError({
						'arrival_date': f'Dates conflict with existing reservation from {existing_booking.arrival_date} to {existing_booking.departure_date}'
					})
		
		return data


class TransactionDataSerializer(serializers.ModelSerializer):
	reservation_info = ReservationDataSerializer(source='reservation', read_only=True)
	
	class Meta:
		model = Payment
		fields = ['id', 'reservation', 'reservation_info', 'transaction_amount', 'payment_state', 'processed_at']
		read_only_fields = ['id', 'processed_at']
	
	def validate_transaction_amount(self, value):
		if value <= 0:
			raise serializers.ValidationError("Transaction amount must be positive")
		return value


class FeedbackDataSerializer(serializers.ModelSerializer):
	reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
	listing_name = serializers.CharField(source='reviewed_property.listing_title', read_only=True)
	
	class Meta:
		model = Review
		fields = [
			'id', 'reviewer', 'reviewer_username', 'reviewed_property', 'listing_name',
			'associated_booking', 'rating_score', 'review_text'
		]
		read_only_fields = ['id', 'reviewer']
	
	def validate_rating_score(self, value):
		if not (1 <= value <= 5):
			raise serializers.ValidationError("Rating score must be within 1-5 range")
		return value
	
	def validate(self, data):
		current_user = self.context['request'].user
		target_property = data.get('reviewed_property')
		linked_booking = data.get('associated_booking')
		
		if linked_booking:
			if linked_booking.guest != current_user:
				raise serializers.ValidationError({
					'associated_booking': 'Reviews limited to your own reservations'
				})
				
			if linked_booking.reserved_property != target_property:
				raise serializers.ValidationError({
					'reviewed_property': 'Property mismatch with selected reservation'
				})
				
			if linked_booking.reservation_state not in ['approved', 'completed']:
				raise serializers.ValidationError({
					'associated_booking': 'Reviews restricted to approved or completed stays'
				})
				
			if linked_booking.departure_date > date.today():
				raise serializers.ValidationError({
					'associated_booking': 'Cannot review upcoming reservations'
				})
		
		if not self.instance:
			duplicate_check = Review.objects.filter(
				reviewer=current_user,
				reviewed_property=target_property
			)
			
			if linked_booking:
				duplicate_check = duplicate_check.filter(associated_booking=linked_booking)
			
			if duplicate_check.exists():
				raise serializers.ValidationError({
					'reviewed_property': 'You have already submitted a review for this'
				})
		
		return data


class SavedListingsSerializer(serializers.ModelSerializer):
	saved_properties = ListingDataSerializer(many=True, read_only=True)
	total_items = serializers.SerializerMethodField()
	
	class Meta:
		model = Wishlist
		fields = ['id', 'owner', 'list_name', 'saved_properties', 'total_items', 'created_on']
		read_only_fields = ['id', 'owner', 'created_on']
	
	def get_total_items(self, obj):
		return obj.saved_properties.count()


class LocationDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ['id', 'account_owner', 'address_category', 'street_line', 'city_name', 'state_province', 'postal_code', 'country_name', 'primary_address', 'created_at']
		read_only_fields = ['id', 'account_owner', 'created_at']


class UserPreferenceSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerPreferences
		fields = ['id', 'account', 'budget_min', 'budget_max', 'favorite_destinations', 'desired_amenities', 'enable_email_alerts', 'enable_sms_alerts', 'subscribe_newsletter', 'preference_set_on']
		read_only_fields = ['id', 'account', 'preference_set_on']


class AccountCreationSerializer(serializers.ModelSerializer):
	secret_code = serializers.CharField(write_only=True, min_length=8)
	confirm_secret = serializers.CharField(write_only=True, min_length=8)

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'secret_code', 'confirm_secret']

	def validate(self, data):
		if data['secret_code'] != data.pop('confirm_secret'):
			raise serializers.ValidationError({
				"secret_code": "Password confirmation does not match"
			})
		
		if len(data['secret_code']) < 8:
			raise serializers.ValidationError({
				"secret_code": "Password must contain at least 8 characters"
			})
		
		if data['username'] and User.objects.filter(username__iexact=data['username']).exists():
			raise serializers.ValidationError({
				"username": "This username is already registered"
			})
		
		if data.get('email') and User.objects.filter(email__iexact=data['email']).exists():
			raise serializers.ValidationError({
				"email": "This email address is already in use"
			})
		
		return data

	def create(self, validated_data):
		secret = validated_data.pop('secret_code')
		account = User.objects.create_user(
			username=validated_data['username'],
			email=validated_data.get('email', ''),
			first_name=validated_data.get('first_name', ''),
			last_name=validated_data.get('last_name', ''),
			password=secret
		)
		
		UserProfile.objects.filter(user=account).update(
			user_role='guest',
			full_name=f"{account.first_name} {account.last_name}".strip() or account.username,
			contact_email=account.email
		)
		
		CustomerPreferences.objects.create(account=account)
		
		return account


class AuthenticationSerializer(serializers.Serializer):
	account_name = serializers.CharField()
	secret_code = serializers.CharField(write_only=True)
