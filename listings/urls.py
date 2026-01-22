
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
	ProfileManagementViewSet, ListingManagementViewSet, PhotoManagementViewSet,
	ReservationManagementViewSet, TransactionViewSet, FeedbackManagementViewSet, 
	SavedPropertiesViewSet, AccountAuthViewSet, LocationManagementViewSet, PreferenceManagementViewSet,
	send_email_notification
)

router = DefaultRouter()
router.register(r'profiles', ProfileManagementViewSet)
router.register(r'listings', ListingManagementViewSet)
router.register(r'photos', PhotoManagementViewSet)
router.register(r'reservations', ReservationManagementViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'feedback', FeedbackManagementViewSet)
router.register(r'saved-collections', SavedPropertiesViewSet)
router.register(r'account-auth', AccountAuthViewSet, basename='account-auth')
router.register(r'locations', LocationManagementViewSet, basename='location')
router.register(r'user-preferences', PreferenceManagementViewSet, basename='user-preferences')

urlpatterns = [
	path('', include(router.urls)),
	path('send-email/', send_email_notification, name='send-email'),
	path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]