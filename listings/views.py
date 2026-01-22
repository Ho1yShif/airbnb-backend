from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import date
from .models import UserProfile, Property, PropertyImage, Booking, Payment, Review, Wishlist, Address, CustomerPreferences
from .serializers import (
	ProfileDataSerializer, ListingDataSerializer, ListingPhotoSerializer,
	ReservationDataSerializer, TransactionDataSerializer, FeedbackDataSerializer, SavedListingsSerializer,
	LocationDataSerializer, UserPreferenceSerializer, AccountCreationSerializer, AuthenticationSerializer,
	EmailNotificationSerializer
)
from .permissions import IsOwnerOrReadOnly, IsHostOrReadOnly, IsBookingOwner
from .tasks import send_notification_email


class ProfileManagementViewSet(viewsets.ModelViewSet):
	queryset = UserProfile.objects.all()
	serializer_class = ProfileDataSerializer
	permission_classes = [IsAuthenticated]
	
	def get_queryset(self):
		if self.request.user.is_staff:
			return UserProfile.objects.all()
		return UserProfile.objects.filter(user=self.request.user)
	
	@action(detail=False, methods=['get'])
	def current_profile(self, request):
		profile = UserProfile.objects.get(user=request.user)
		serializer = self.get_serializer(profile)
		return Response(serializer.data)


class ListingManagementViewSet(viewsets.ModelViewSet):
	queryset = Property.objects.all()
	serializer_class = ListingDataSerializer
	permission_classes = [IsAuthenticatedOrReadOnly, IsHostOrReadOnly]
	filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
	filterset_fields = ['listing_status', 'property_owner']
	search_fields = ['listing_title', 'property_description', 'property_location']
	ordering_fields = ['nightly_rate', 'listing_title']
	
	def perform_create(self, serializer):
		serializer.save(property_owner=self.request.user)
	
	def get_queryset(self):
		queryset = Property.objects.all()
		
		location_query = self.request.query_params.get('location', None)
		if location_query:
			queryset = queryset.filter(property_location__icontains=location_query)
		
		min_rate = self.request.query_params.get('min_price', None)
		max_rate = self.request.query_params.get('max_price', None)
		if min_rate:
			queryset = queryset.filter(nightly_rate__gte=min_rate)
		if max_rate:
			queryset = queryset.filter(nightly_rate__lte=max_rate)
		
		return queryset
	
	@action(detail=False, methods=['get'])
	def owner_listings(self, request):
		listings = Property.objects.filter(property_owner=request.user)
		serializer = self.get_serializer(listings, many=True)
		return Response(serializer.data)


class PhotoManagementViewSet(viewsets.ModelViewSet):
	queryset = PropertyImage.objects.all()
	serializer_class = ListingPhotoSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	
	def get_queryset(self):
		queryset = PropertyImage.objects.all()
		listing_id = self.request.query_params.get('listing', None)
		if listing_id:
			queryset = queryset.filter(listing_id=listing_id)
		return queryset


class ReservationManagementViewSet(viewsets.ModelViewSet):
	queryset = Booking.objects.all()
	serializer_class = ReservationDataSerializer
	permission_classes = [IsAuthenticated, IsBookingOwner]
	filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
	filterset_fields = ['reservation_state', 'reserved_property']
	ordering_fields = ['arrival_date', 'departure_date']
	
	def get_queryset(self):
		current_user = self.request.user
		if current_user.is_staff:
			return Booking.objects.all()
		return Booking.objects.filter(
			Q(guest=current_user) | Q(reserved_property__property_owner=current_user)
		)
	
	def perform_create(self, serializer):
		serializer.save(guest=self.request.user)
	
	@action(detail=True, methods=['post'])
	def approve_reservation(self, request, pk=None):
		reservation = self.get_object()
		if reservation.reserved_property.property_owner != request.user:
			return Response(
				{'error': 'Only listing owner can approve reservations'},
				status=status.HTTP_403_FORBIDDEN
			)
		reservation.reservation_state = 'approved'
		reservation.save()
		return Response({'status': 'reservation approved'})
	
	@action(detail=True, methods=['post'])
	def cancel_reservation(self, request, pk=None):
		reservation = self.get_object()
		reservation.reservation_state = 'cancelled'
		reservation.save()
		return Response({'status': 'reservation cancelled'})


class TransactionViewSet(viewsets.ModelViewSet):
	queryset = Payment.objects.all()
	serializer_class = TransactionDataSerializer
	permission_classes = [IsAuthenticated]
	
	def get_queryset(self):
		current_user = self.request.user
		if current_user.is_staff:
			return Payment.objects.all()
		return Payment.objects.filter(reservation__guest=current_user)


class FeedbackManagementViewSet(viewsets.ModelViewSet):
	queryset = Review.objects.all()
	serializer_class = FeedbackDataSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
	filterset_fields = ['reviewed_property', 'rating_score']
	ordering_fields = ['rating_score']
	
	def get_queryset(self):
		queryset = Review.objects.all()
		property_filter = self.request.query_params.get('property', None)
		if property_filter:
			queryset = queryset.filter(reviewed_property_id=property_filter)
		return queryset
	
	def perform_create(self, serializer):
		serializer.save(reviewer=self.request.user)


class SavedPropertiesViewSet(viewsets.ModelViewSet):
	queryset = Wishlist.objects.all()
	serializer_class = SavedListingsSerializer
	permission_classes = [IsAuthenticated]
	
	def get_queryset(self):
		return Wishlist.objects.filter(owner=self.request.user)
	
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
	
	@action(detail=True, methods=['post'])
	def add_to_list(self, request, pk=None):
		collection = self.get_object()
		listing_id = request.data.get('property_id')
		
		if not listing_id:
			return Response(
				{'error': 'property_id field is mandatory'},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		try:
			property_instance = Property.objects.get(pk=listing_id)
			
			if property_instance in collection.saved_properties.all():
				return Response(
					{'message': 'Property already exists in this collection'},
					status=status.HTTP_200_OK
				)
			
			collection.saved_properties.add(property_instance)
			
			return Response({
				'message': 'Property successfully added to collection',
				'collection_size': collection.saved_properties.count()
			}, status=status.HTTP_200_OK)
			
		except Property.DoesNotExist:
			return Response(
				{'error': f'Property with ID {listing_id} does not exist'},
				status=status.HTTP_404_NOT_FOUND
			)
		except ValueError:
			return Response(
				{'error': 'Invalid property_id format'},
				status=status.HTTP_400_BAD_REQUEST
			)
	
	@action(detail=True, methods=['post'])
	def remove_from_list(self, request, pk=None):
		collection = self.get_object()
		listing_id = request.data.get('property_id')
		
		if not listing_id:
			return Response(
				{'error': 'property_id field is mandatory'},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		try:
			property_instance = Property.objects.get(pk=listing_id)
			
			if property_instance not in collection.saved_properties.all():
				return Response(
					{'error': 'Property not found in this collection'},
					status=status.HTTP_404_NOT_FOUND
				)
			
			collection.saved_properties.remove(property_instance)
			
			return Response({
				'message': 'Property removed from collection',
				'collection_size': collection.saved_properties.count()
			}, status=status.HTTP_200_OK)
			
		except Property.DoesNotExist:
			return Response(
				{'error': f'Property with ID {listing_id} does not exist'},
				status=status.HTTP_404_NOT_FOUND
			)
		except ValueError:
			return Response(
				{'error': 'Invalid property_id format'},
				status=status.HTTP_400_BAD_REQUEST
			)


class AccountAuthViewSet(viewsets.ViewSet):
	permission_classes = [AllowAny]

	@action(detail=False, methods=['post'])
	def create_account(self, request):
		serializer = AccountCreationSerializer(data=request.data, context={'request': request})
		
		if not serializer.is_valid():
			return Response(
				serializer.errors,
				status=status.HTTP_400_BAD_REQUEST
			)
		
		account = serializer.save()
		auth_token, _ = Token.objects.get_or_create(user=account)
		
		profile_data = {
			'user_id': account.id,
			'username': account.username,
			'email': account.email,
			'full_name': account.get_full_name() or account.username,
			'access_token': auth_token.key,
			'account_status': 'active',
			'created_at': account.date_joined.isoformat()
		}
		
		return Response(profile_data, status=status.HTTP_201_CREATED)

	@action(detail=False, methods=['post'])
	def authenticate(self, request):
		serializer = AuthenticationSerializer(data=request.data)
		
		if not serializer.is_valid():
			return Response(
				serializer.errors,
				status=status.HTTP_400_BAD_REQUEST
			)
		
		credentials = serializer.validated_data
		user_account = authenticate(
			username=credentials['account_name'],
			password=credentials['secret_code']
		)
		
		if not user_account:
			return Response(
				{'error': 'Invalid credentials provided'},
				status=status.HTTP_401_UNAUTHORIZED
			)
		
		if not user_account.is_active:
			return Response(
				{'error': 'Account has been deactivated'},
				status=status.HTTP_403_FORBIDDEN
			)
		
		auth_token, token_created = Token.objects.get_or_create(user=user_account)
		
		profile_info = {
			'user_id': user_account.id,
			'username': user_account.username,
			'email': user_account.email,
			'full_name': user_account.get_full_name(),
			'access_token': auth_token.key,
			'token_type': 'Token',
			'user_role': getattr(user_account.profile, 'user_role', 'guest')
		}
		
		return Response(profile_info, status=status.HTTP_200_OK)

	@action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
	def terminate_session(self, request):
		try:
			request.user.auth_token.delete()
			return Response({
				'message': 'Session terminated successfully',
				'logout_time': date.today().isoformat()
			}, status=status.HTTP_200_OK)
		except Exception as e:
			return Response(
				{'error': 'Session termination failed'},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)


class LocationManagementViewSet(viewsets.ModelViewSet):
	serializer_class = LocationDataSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Address.objects.filter(account_owner=self.request.user)

	def perform_create(self, serializer):
		serializer.save(account_owner=self.request.user)


class PreferenceManagementViewSet(viewsets.ModelViewSet):
	serializer_class = UserPreferenceSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return CustomerPreferences.objects.filter(account=self.request.user)

	@action(detail=False, methods=['get'])
	def current_preferences(self, request):
		preferences, created = CustomerPreferences.objects.get_or_create(account=request.user)
		serializer = self.get_serializer(preferences)
		return Response(serializer.data)


@api_view(['POST'])
def send_email_notification(request):
	"""
	Send email notification via Celery task.
	Expects: {"subject": "...", "message": "...", "recipient": "..."}
	"""
	serializer = EmailNotificationSerializer(data=request.data)
	if serializer.is_valid():
		try:
			# Queue the email task asynchronously
			task = send_notification_email.delay(
				subject=serializer.validated_data['subject'],
				message=serializer.validated_data['message'],
				recipient=serializer.validated_data['recipient']
			)
			return Response(
				{
					'status': 'success',
					'message': 'Email task queued successfully',
					'task_id': task.id
				},
				status=status.HTTP_202_ACCEPTED
			)
		except Exception as e:
			return Response(
				{'status': 'error', 'message': str(e)},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
	
	return Response(
		{
			'status': 'error',
			'message': 'Invalid data',
			'errors': serializer.errors
		},
		status=status.HTTP_400_BAD_REQUEST
	)

