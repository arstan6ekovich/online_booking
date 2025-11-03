from django.contrib import admin
from django.urls import path, include
from rest_framework import generics, viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import (
    Country, City, Hotel, UserProfile,
    Room, Review, Booking, Favorite, FavoriteItem
)
from .serializers import (
    CountrySerializer, UserProfileSerializer, HotelListSerializer, HotelDetailSerializer,
    HotelHTTPSerializer, CityListSerializer, CityDetailSerializer, RoomCreateSerializer,
    ReviewSerializer, BookingListSerializer, BookingHTTPSerializer,
    FavoriteListSerializer, FavoriteHTTPSerializer, FavoriteItemListSerializer,
    FavoriteItemHTTPSerializer, UserSerializer, LoginSerializer
)
from .permissions import CheckStatus, ReviewPermissions, CheckOwner
from .filters import HotelFilter, RoomFilter


# ---------- AUTH ----------
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # нужно для Swagger, чтобы не падал при генерации схемы
        if getattr(self, 'swagger_fake_view', False):
            return Response(status=status.HTTP_200_OK)

        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class UserProfileViewSets(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


# ---------- COUNTRY ----------
class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated, CheckStatus]


# ---------- CITY ----------
class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer
    permission_classes = [permissions.IsAuthenticated]


class CityDetailAPIView(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


# ---------- HOTEL ----------
class HotelListView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter


class HotelDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class HotelCreateAPIView(generics.CreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelHTTPSerializer
    permission_classes = [permissions.IsAuthenticated, CheckStatus]


class HotelUpdateAPIView(generics.UpdateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelHTTPSerializer
    permission_classes = [permissions.IsAuthenticated, CheckStatus]


# ---------- ROOM ----------
class RoomCreateAPIView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer
    permission_classes = [permissions.IsAuthenticated, CheckStatus]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter


# ---------- REVIEW ----------
class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, ReviewPermissions]


# ---------- BOOKING ----------
class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]


class BookingDetailAPIView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]


class BookingUpdateAPIView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingHTTPSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]


class BookingDeleteAPIView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingHTTPSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]


# ---------- FAVORITE ----------
class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]


class FavoriteCreateAPIView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteHTTPSerializer
    permission_classes = [permissions.IsAuthenticated, ReviewPermissions]


class FavoriteUpdateAPIView(generics.UpdateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteHTTPSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]


class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteHTTPSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]


# ---------- FAVORITE ITEM ----------
class FavoriteItemListView(generics.ListAPIView):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemListSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]


class FavoriteItemCreateAPIView(generics.CreateAPIView):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemHTTPSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]


class FavoriteItemUpdateAPIView(generics.UpdateAPIView):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemHTTPSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]


class FavoriteItemDeleteAPIView(generics.DestroyAPIView):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemHTTPSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOwner]
