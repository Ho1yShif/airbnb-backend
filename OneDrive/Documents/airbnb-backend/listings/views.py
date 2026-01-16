"""
API ViewSets for AirBnB Backend - Property Rental Platform

Author: Martin Mawien
Copyright (c) 2026 Martin Mawien
GitHub: https://github.com/Martin-Mawien/airbnb-backend

This module provides REST API endpoints for:
- User profiles
- Property listings with search and filtering
- Booking management
- Payment processing
- Reviews and ratings
- Wishlist functionality
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import UserProfile, Property, PropertyImage, Booking, Payment, Review, Wishlist
from .serializers import (
	UserProfileSerializer, PropertySerializer, PropertyImageSerializer,
	BookingSerializer, PaymentSerializer, ReviewSerializer, WishlistSerializer
)
from .permissions import IsOwnerOrReadOnly, IsHostOrReadOnly, IsBookingOwner


class UserProfileViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for user profiles.
	Users can only view and update their own profile.
	"""
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = [IsAuthenticated]
	
	def get_queryset(self):
		# Users can only see their own profile unless they're admin
		if self.request.user.is_staff:
			return UserProfile.objects.all()
		return UserProfile.objects.filter(user=self.request.user)
	
	@action(detail=False, methods=['get'])
	def me(self, request):
		"""Get current user's profile"""
		profile = UserProfile.objects.get(user=request.user)
		serializer = self.get_serializer(profile)
		return Response(serializer.data)


class PropertyViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for properties.
	Anyone can view properties, but only hosts can create/update/delete their own.
	"""
	queryset = Property.objects.all()
	serializer_class = PropertySerializer
	permission_classes = [IsAuthenticatedOrReadOnly, IsHostOrReadOnly]
	filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
	filterset_fields = ['status', 'owner']
	search_fields = ['title', 'description', 'location']
	ordering_fields = ['price', 'title']
	
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
	
	def get_queryset(self):
		queryset = Property.objects.all()
		
		# Filter by location (partial match)
		location = self.request.query_params.get('location', None)
		if location:
			queryset = queryset.filter(location__icontains=location)
		
		# Filter by price range
		min_price = self.request.query_params.get('min_price', None)
		max_price = self.request.query_params.get('max_price', None)
		if min_price:
			queryset = queryset.filter(price__gte=min_price)
		if max_price:
			queryset = queryset.filter(price__lte=max_price)
		
		return queryset
	
	@action(detail=False, methods=['get'])
	def my_properties(self, request):
		"""Get current user's properties"""
		properties = Property.objects.filter(owner=request.user)
		serializer = self.get_serializer(properties, many=True)
		return Response(serializer.data)


class PropertyImageViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for property images.
	Only property owners can add/update/delete images.
	"""
	queryset = PropertyImage.objects.all()
	serializer_class = PropertyImageSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	
	def get_queryset(self):
		queryset = PropertyImage.objects.all()
		property_id = self.request.query_params.get('property', None)
		if property_id:
			queryset = queryset.filter(property_id=property_id)
		return queryset


class BookingViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for bookings.
	Users can only view and manage their own bookings.
	"""
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticated, IsBookingOwner]
	filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
	filterset_fields = ['status', 'property']
	ordering_fields = ['check_in_date', 'check_out_date']
	
	def get_queryset(self):
		user = self.request.user
		# Users see their own bookings
		# Hosts see bookings for their properties
		if user.is_staff:
			return Booking.objects.all()
		return Booking.objects.filter(
			Q(user=user) | Q(property__owner=user)
		)
	
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
	
	@action(detail=True, methods=['post'])
	def confirm(self, request, pk=None):
		"""Confirm a booking (host only)"""
		booking = self.get_object()
		if booking.property.owner != request.user:
			return Response(
				{'error': 'Only the property owner can confirm bookings'},
				status=status.HTTP_403_FORBIDDEN
			)
		booking.status = 'confirmed'
		booking.save()
		return Response({'status': 'booking confirmed'})
	
	@action(detail=True, methods=['post'])
	def cancel(self, request, pk=None):
		"""Cancel a booking"""
		booking = self.get_object()
		booking.status = 'cancelled'
		booking.save()
		return Response({'status': 'booking cancelled'})


class PaymentViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for payments.
	Users can only view their own payments.
	"""
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer
	permission_classes = [IsAuthenticated]
	
	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return Payment.objects.all()
		return Payment.objects.filter(booking__user=user)


class ReviewViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for reviews.
	Anyone can read reviews, but only users who have booked can write them.
	"""
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
	filterset_fields = ['property', 'rating']
	ordering_fields = ['rating']
	
	def get_queryset(self):
		queryset = Review.objects.all()
		property_id = self.request.query_params.get('property', None)
		if property_id:
			queryset = queryset.filter(property_id=property_id)
		return queryset
	
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class WishlistViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for wishlists.
	Users can only view and manage their own wishlists.
	"""
	queryset = Wishlist.objects.all()
	serializer_class = WishlistSerializer
	permission_classes = [IsAuthenticated]
	
	def get_queryset(self):
		return Wishlist.objects.filter(user=self.request.user)
	
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
	
	@action(detail=True, methods=['post'])
	def add_property(self, request, pk=None):
		"""Add a property to wishlist"""
		wishlist = self.get_object()
		property_id = request.data.get('property_id')
		if property_id:
			try:
				property_obj = Property.objects.get(id=property_id)
				wishlist.properties.add(property_obj)
				return Response({'status': 'property added to wishlist'})
			except Property.DoesNotExist:
				return Response(
					{'error': 'Property not found'},
					status=status.HTTP_404_NOT_FOUND
				)
		return Response(
			{'error': 'property_id required'},
			status=status.HTTP_400_BAD_REQUEST
		)
	
	@action(detail=True, methods=['post'])
	def remove_property(self, request, pk=None):
		"""Remove a property from wishlist"""
		wishlist = self.get_object()
		property_id = request.data.get('property_id')
		if property_id:
			try:
				property_obj = Property.objects.get(id=property_id)
				wishlist.properties.remove(property_obj)
				return Response({'status': 'property removed from wishlist'})
			except Property.DoesNotExist:
				return Response(
					{'error': 'Property not found'},
					status=status.HTTP_404_NOT_FOUND
				)
		return Response(
			{'error': 'property_id required'},
			status=status.HTTP_400_BAD_REQUEST
		)

