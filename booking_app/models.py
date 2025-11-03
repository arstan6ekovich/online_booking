from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    country_name = models.CharField(max_length=64, unique=True)
    country_image = models.ImageField(upload_to='country_image/')

    def __str__(self):
        return self.country_name


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'client'),
        ('owner', 'owner'),
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(12), MaxValueValidator(85)],
        null=True,
        blank=True
    )
    user_phone_number = PhoneNumberField(null=True, blank=True)
    user_image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    user_role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='client')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} ({self.user_role})'


class City(models.Model):
    city_name = models.CharField(max_length=64, unique=True)
    city_image = models.ImageField(upload_to='city_image/')

    def __str__(self):
        return self.city_name


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=64)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    hotel_star = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    description = models.TextField()
    street = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hotel_name} — {self.city} ★{self.hotel_star}'

    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum([i.stars for i in ratings]) / ratings.count(), 1)
        return 0

    def get_count_people(self):
        return self.reviews.count()


class Service(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=64, unique=True)
    service_logo = models.ImageField(upload_to='service_logo/')

    def __str__(self):
        return f'{self.service_name} ({self.hotel.hotel_name})'


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
    hotel_images = models.ImageField(upload_to='hotel_images/')
    created_image = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel.hotel_name} — {self.created_image}'


class Room(models.Model):
    room_number = models.PositiveSmallIntegerField()
    room_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    TYPE_CHOICES = (
        ('люкс', 'люкс'),
        ('семейный', 'семейный'),
        ('одноместный', 'одноместный'),
        ('двухместный', 'двухместный'),
    )
    room_type = models.CharField(max_length=16, choices=TYPE_CHOICES, default='люкс')

    STATUS_CHOICES = (
        ('свободен', 'свободен'),
        ('забронирован', 'забронирован'),
        ('занят', 'занят'),
    )
    room_status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='свободен')
    room_price = models.PositiveIntegerField()
    room_description = models.TextField()

    def __str__(self):
        return f'{self.room_hotel.hotel_name} — №{self.room_number} ({self.room_type})'


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_images = models.ImageField(upload_to='room_images/')
    created_image = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.room.room_hotel.hotel_name} — {self.created_image}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    stars = models.PositiveSmallIntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)



class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    total_price = models.PositiveIntegerField(default=0)
    STATUS_BOOK_CHOICES = (
        ('отменено', 'отменено'),
        ('подтверждено', 'подтверждено'),
    )
    status_book = models.CharField(max_length=16, choices=STATUS_BOOK_CHOICES)

    def __str__(self):
        return f'{self.user.username} — {self.hotel.hotel_name} ({self.status_book})'


class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'Избранное {self.user.username}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.favorite.user.username} - {self.hotel.hotel_name}'
