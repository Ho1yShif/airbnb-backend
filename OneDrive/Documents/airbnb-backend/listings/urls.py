from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user-profiles', views.UserProfileViewSet)
router.register(r'properties', views.PropertyViewSet)
router.register(r'property-images', views.PropertyImageViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'wishlists', views.WishlistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]