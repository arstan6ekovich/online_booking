from rest_framework import serializers
from .models import (
    Country, UserProfile, City, Hotel, HotelImage,
    Service, Room, RoomImage, Review, Booking, Favorite, FavoriteItem
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# ---------- AUTH ----------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'username', 'email', 'country', 'password',
            'first_name', 'last_name', 'age', 'user_image',
            'user_phone_number', 'user_role', 'created_date'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'id': instance.id,
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise serializers.ValidationError("Неверные учетные данные")

        refresh = RefreshToken.for_user(user)
        return {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    def to_representation(self, instance):
        return instance


# ---------- BASE SERIALIZERS ----------
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'country_name', 'country_image')


class UserProfileSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'country', 'first_name', 'last_name',
            'age', 'user_phone_number', 'user_image',
            'user_role', 'created_date'
        )


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city_name', 'city_image')


class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city_name', 'city_image')


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ('hotel_images', 'created_image')


class HotelDetailSerializer(serializers.ModelSerializer):
    city = CityDetailSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    owner = UserProfileSerializer(read_only=True)
    hotel_images = HotelImageSerializer(many=True, read_only=True)
    count_people = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = (
            'id', 'hotel_name', 'city', 'hotel_star', 'description', 'street',
            'country', 'owner', 'hotel_images', 'avg_rating', 'count_people'
        )

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class HotelListSerializer(serializers.ModelSerializer):
    city = CityDetailSerializer(read_only=True)
    hotel_images = HotelImageSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ('id', 'hotel_name', 'city', 'hotel_star', 'street', 'hotel_images')


class HotelHTTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomListSerializer(serializers.ModelSerializer):
    room_hotel = HotelListSerializer(read_only=True)

    class Meta:
        model = Room
        fields = (
            'id', 'room_number', 'room_hotel',
            'room_type', 'room_status', 'room_price', 'room_description'
        )


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class BookingListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    hotel = HotelListSerializer(read_only=True)
    room = RoomListSerializer(read_only=True)
    check_out = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    check_in = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Booking
        fields = (
            'id', 'check_in', 'check_out', 'total_price',
            'status_book', 'user', 'hotel', 'room'
        )


class BookingHTTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class FavoriteListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'user')


class FavoriteHTTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteItemListSerializer(serializers.ModelSerializer):
    favorite = FavoriteListSerializer(read_only=True)
    hotel = HotelListSerializer(read_only=True)

    class Meta:
        model = FavoriteItem
        fields = ('id', 'quantity', 'favorite', 'hotel')


class FavoriteItemHTTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'
