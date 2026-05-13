from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Cuisine(models.Model):
    """Restaurant oshxonasi turlari: o'zbek, xitoy, italyan, etc."""
    name_uz = models.CharField(max_length=80, verbose_name="Nomi (UZ)")
    name_en = models.CharField(max_length=80, verbose_name="Nomi (EN)", blank=True)
    name_ru = models.CharField(max_length=80, verbose_name="Nomi (RU)", blank=True)
    icon = models.CharField(max_length=10, default='🍽️')

    class Meta:
        verbose_name = "Oshxona turi"
        verbose_name_plural = "Oshxona turlari"
        ordering = ['name_uz']

    def __str__(self):
        return f"{self.icon} {self.name_uz}"


class Restaurant(models.Model):
    PRICE_CHOICES = [
        ('$', 'Arzon'),
        ('$$', "O'rtacha"),
        ('$$$', 'Qimmat'),
        ('$$$$', 'Premium'),
    ]
    CITY_CHOICES = [
        ('khiva', 'Xiva'),
        ('urgench', 'Urganch'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nomi")
    name_en = models.CharField(max_length=200, blank=True)
    name_ru = models.CharField(max_length=200, blank=True)

    description_uz = models.TextField(verbose_name="Tavsif (UZ)")
    description_en = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)

    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants', verbose_name="Oshxona turlari")
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    price_range = models.CharField(max_length=4, choices=PRICE_CHOICES, default='$$')
    rating = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Reyting (0-5)"
    )

    address = models.CharField(max_length=300)
    address_en = models.CharField(max_length=300, blank=True)
    address_ru = models.CharField(max_length=300, blank=True)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True, verbose_name="Ish vaqti")

    # Xususiyatlar
    has_wifi = models.BooleanField(default=False, verbose_name="WiFi")
    has_parking = models.BooleanField(default=False, verbose_name="Parking")
    has_outdoor_seating = models.BooleanField(default=False, verbose_name="Tashqi joy")
    is_halal = models.BooleanField(default=True, verbose_name="Halol")
    is_vegetarian_friendly = models.BooleanField(default=False, verbose_name="Vegetarian")

    is_featured = models.BooleanField(default=False, verbose_name="Asosiy")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Restoran"
        verbose_name_plural = "Restoranlar"
        ordering = ['-is_featured', '-rating']

    def __str__(self):
        return self.name

    @property
    def cover_image(self):
        cover = self.images.filter(is_cover=True).first()
        return cover or self.images.first()


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='restaurants/')
    is_cover = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_cover', 'order']

    def save(self, *args, **kwargs):
        if self.is_cover:
            RestaurantImage.objects.filter(
                restaurant=self.restaurant, is_cover=True
            ).update(is_cover=False)
        super().save(*args, **kwargs)
