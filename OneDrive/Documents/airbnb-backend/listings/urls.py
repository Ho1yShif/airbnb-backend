
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
	UserProfileViewSet, PropertyViewSet, PropertyImageViewSet,
	BookingViewSet, PaymentViewSet, ReviewViewSet, WishlistViewSet
)

router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'property-images', PropertyImageViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'wishlists', WishlistViewSet)

urlpatterns = [
	path('', include(router.urls)),
	path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]