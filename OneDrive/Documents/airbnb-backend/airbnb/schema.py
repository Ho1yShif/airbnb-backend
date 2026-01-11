import graphene
from graphene_django import DjangoObjectType
from listings.models import UserProfile, Property, Booking, Payment, Review, Wishlist


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile


class PropertyType(DjangoObjectType):
    class Meta:
        model = Property


class BookingType(DjangoObjectType):
    class Meta:
        model = Booking


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review


class WishlistType(DjangoObjectType):
    class Meta:
        model = Wishlist


class Query(graphene.ObjectType):
    user_profiles = graphene.List(UserProfileType)
    properties = graphene.List(PropertyType)
    bookings = graphene.List(BookingType)
    payments = graphene.List(PaymentType)
    reviews = graphene.List(ReviewType)
    wishlists = graphene.List(WishlistType)

    def resolve_user_profiles(self, info):
        return UserProfile.objects.all()

    def resolve_properties(self, info):
        return Property.objects.all()

    def resolve_bookings(self, info):
        return Booking.objects.all()

    def resolve_payments(self, info):
        return Payment.objects.all()

    def resolve_reviews(self, info):
        return Review.objects.all()

    def resolve_wishlists(self, info):
        return Wishlist.objects.all()


schema = graphene.Schema(query=Query)