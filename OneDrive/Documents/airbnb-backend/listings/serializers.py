from rest_framework import serializers
from .models import UserProfile, Property, PropertyImage, Booking, Payment, Review, Wishlist


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'name', 'role', 'phone', 'bio', 'avatar', 'created_at']


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'is_primary', 'created_at']


class PropertySerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'owner', 'owner_username', 'title', 'location', 'price', 'description', 'status']
        read_only_fields = ['owner']


class BookingSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'user_username', 'property', 'property_title', 'check_in_date', 'check_out_date', 'status']
        read_only_fields = ['user']


class PaymentSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='booking.id', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'booking', 'booking_id', 'amount', 'status', 'payment_date']
        read_only_fields = ['payment_date']


class ReviewSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_username', 'property', 'property_title', 'booking', 'rating', 'comment']
        read_only_fields = ['user']


class WishlistSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'user_username', 'name', 'properties', 'created_at']
        read_only_fields = ['user', 'created_at']