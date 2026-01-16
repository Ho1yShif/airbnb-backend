"""
Custom Permission Classes for AirBnB Backend

Author: Martin Mawien
Copyright (c) 2026 Martin Mawien
GitHub: https://github.com/Martin-Mawien/airbnb-backend

Security permissions for role-based access control.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow owners of an object to edit it.
	"""
	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request
		if request.method in permissions.SAFE_METHODS:
			return True
		
		# Write permissions are only allowed to the owner
		return obj.user == request.user


class IsHostOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow hosts to create/edit properties.
	"""
	def has_permission(self, request, view):
		# Read permissions are allowed to any request
		if request.method in permissions.SAFE_METHODS:
			return True
		
		# Write permissions are only allowed to authenticated hosts
		if not request.user.is_authenticated:
			return False
		
		# Check if user has host role
		try:
			profile = request.user.profile
			return profile.role in ['host', 'admin'] or request.user.is_staff
		except:
			return request.user.is_staff
	
	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request
		if request.method in permissions.SAFE_METHODS:
			return True
		
		# Write permissions are only allowed to the owner or admin
		return obj.owner == request.user or request.user.is_staff


class IsBookingOwner(permissions.BasePermission):
	"""
	Custom permission to only allow booking owners or property owners to view/edit bookings.
	"""
	def has_object_permission(self, request, view, obj):
		# Allow if user is the booking owner
		if obj.user == request.user:
			return True
		
		# Allow if user is the property owner
		if obj.property.owner == request.user:
			return True
		
		# Allow if user is admin
		return request.user.is_staff
