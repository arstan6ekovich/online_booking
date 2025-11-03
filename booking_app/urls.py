from django.urls import path, include
from rest_framework import routers
from .views import (
    RegisterView, CustomLoginView, LogoutView, UserProfileMeView,
    CityListView, CityDetailAPIView,
    HotelListView, HotelDetailAPIView, HotelCreateAPIView, HotelUpdateAPIView,
    RoomCreateAPIView, ReviewCreateAPIView,
    BookingListView, BookingDetailAPIView, BookingUpdateAPIView, BookingDeleteAPIView,
    FavoriteListView, FavoriteCreateAPIView, FavoriteUpdateAPIView, FavoriteDeleteView,
    FavoriteItemListView, FavoriteItemCreateAPIView, FavoriteItemUpdateAPIView, FavoriteItemDeleteAPIView
)

router = routers.SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),

    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/user/', UserProfileMeView.as_view(), name='user_profile'),

    path('city/', CityListView.as_view(), name='city_list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(), name='city_detail'),

    path('hotel/', HotelListView.as_view(), name='hotel_list'),
    path('hotel/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel_detail'),
    path('hotel/create/', HotelCreateAPIView.as_view(), name='hotel_create'),
    path('hotel/update/<int:pk>/', HotelUpdateAPIView.as_view(), name='hotel_update'),

    path('room/', RoomCreateAPIView.as_view(), name='room_create'),

    path('review/', ReviewCreateAPIView.as_view(), name='review_create'),

    path('booking/', BookingListView.as_view(), name='booking_list'),
    path('booking/<int:pk>/', BookingDetailAPIView.as_view(), name='booking_detail'),
    path('booking/update/<int:pk>/', BookingUpdateAPIView.as_view(), name='booking_update'),
    path('booking/delete/<int:pk>/', BookingDeleteAPIView.as_view(), name='booking_delete'),

    path('favorite/', FavoriteListView.as_view(), name='favorite_list'),
    path('favorite/create/', FavoriteCreateAPIView.as_view(), name='favorite_create'),
    path('favorite/update/<int:pk>/', FavoriteUpdateAPIView.as_view(), name='favorite_update'),
    path('favorite/delete/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite_delete'),

    path('favorite_item/', FavoriteItemListView.as_view(), name='favorite_item_list'),
    path('favorite_item/create/', FavoriteItemCreateAPIView.as_view(), name='favorite_item_create'),
    path('favorite_item/update/<int:pk>/', FavoriteItemUpdateAPIView.as_view(), name='favorite_item_update'),
    path('favorite_item/delete/<int:pk>/', FavoriteItemDeleteAPIView.as_view(), name='favorite_item_delete'),
]
