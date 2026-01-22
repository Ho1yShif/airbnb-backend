"""
Role-based access control permissions for property rental platform.

Implements security policies for user actions based on authentication status
and user roles within the marketplace.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
	
	def has_object_permission(self, request, view, obj):
		if request.method in ('GET', 'HEAD', 'OPTIONS'):
			return True
		
		if not request.user or not request.user.is_authenticated:
			return False
		
		return getattr(obj, 'user', None) == request.user or request.user.is_staff


class IsHostOrReadOnly(permissions.BasePermission):
	
	def has_permission(self, request, view):
		if request.method in ('GET', 'HEAD', 'OPTIONS'):
			return True
		
		if not request.user or not request.user.is_authenticated:
			return False
		
		if request.user.is_superuser:
			return True
		
		try:
			user_profile = getattr(request.user, 'profile', None)
			if user_profile:
				return user_profile.user_role in ('host', 'admin')
			return False
		except Exception:
			return False
	
	def has_object_permission(self, request, view, obj):
		if request.method in ('GET', 'HEAD', 'OPTIONS'):
			return True
		
		if request.user.is_superuser:
			return True
		
		owner_field = getattr(obj, 'property_owner', None) or getattr(obj, 'owner', None)
		return owner_field == request.user if owner_field else False


class IsBookingOwner(permissions.BasePermission):
	
	def has_object_permission(self, request, view, obj):
		if not request.user or not request.user.is_authenticated:
			return False
		
		if request.user.is_superuser:
			return True
		
		if hasattr(obj, 'guest') and obj.guest == request.user:
			return True
		
		if hasattr(obj, 'reserved_property'):
			property_owner = getattr(obj.reserved_property, 'property_owner', None)
			if property_owner == request.user:
				return True
		
		return False
