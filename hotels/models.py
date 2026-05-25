from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Amenity(models.Model):
    name_uz = models.CharField(max_length=100, verbose_name="Nomi (UZ)")
    name_en = models.CharField(max_length=100, verbose_name="Nomi (EN)")
    name_ru = models.CharField(max_length=100, verbose_name="Nomi (RU)")
    icon    = models.CharField(max_length=10, help_text="Emoji belgisi, masalan: 🏊")

    class Meta:
        verbose_name        = "Qulaylik"
        verbose_name_plural = "Qulayliklar"
        ordering            = ['name_uz']
        indexes = [
            models.Index(fields=['name_uz'], name='amenity_name_uz_idx'),
        ]

    def __str__(self):
        return f"{self.icon} {self.name_uz}"

    def get_name(self, lang='uz'):
        return getattr(self, f'name_{lang}', self.name_uz) or self.name_uz


class Hotel(models.Model):
    CITY_CHOICES = [
        ('urgench', 'Urganch'),
        ('khiva',   'Xiva'),
    ]

    # ── Nom (ko'p tilli) ─────────────────────────────────────
    name    = models.CharField(max_length=200, verbose_name="Nomi (asosiy)")
    name_en = models.CharField(max_length=200, blank=True, verbose_name="Nomi (EN)")
    name_ru = models.CharField(max_length=200, blank=True, verbose_name="Nomi (RU)")

    city            = models.CharField(max_length=20, choices=CITY_CHOICES, verbose_name="Shahar")
    stars           = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Yulduzlar soni",
    )
    rating          = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="Reyting (0–10)",
    )
    price_per_night = models.PositiveIntegerField(verbose_name="Bir kechaga narx (UZS)")
    address         = models.CharField(max_length=300, verbose_name="Manzil")
    address_en      = models.CharField(max_length=300, blank=True, verbose_name="Manzil (EN)")
    address_ru      = models.CharField(max_length=300, blank=True, verbose_name="Manzil (RU)")
    latitude        = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        verbose_name="Kenglik (lat)",
    )
    longitude       = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        verbose_name="Uzunlik (lng)",
    )
    google_maps_url = models.URLField(blank=True, verbose_name="Google Maps havolasi")

    # ── Tavsif (ko'p tilli) ──────────────────────────────────
    description_uz  = models.TextField(verbose_name="Tavsif (UZ)")
    description_en  = models.TextField(blank=True, verbose_name="Tavsif (EN)")
    description_ru  = models.TextField(blank=True, verbose_name="Tavsif (RU)")

    amenities       = models.ManyToManyField(Amenity, blank=True, verbose_name="Qulayliklar")
    is_featured     = models.BooleanField(default=False, verbose_name="Tavsiya etilgan?")
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Mehmonxona"
        verbose_name_plural = "Mehmonxonalar"
        ordering            = ['-is_featured', '-rating']
        indexes = [
            models.Index(fields=['city'], name='hotel_city_idx'),
            models.Index(fields=['is_featured', '-rating'], name='hotel_featured_rating_idx'),
            models.Index(fields=['stars'], name='hotel_stars_idx'),
            models.Index(fields=['price_per_night'], name='hotel_price_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_city_display()}, {self.stars}★)"

    def get_name(self, lang='uz'):
        """So'ralgan tildagi nomni qaytaradi, topilmasa uzbekcha nom"""
        if lang == 'uz':
            return self.name
        return getattr(self, f'name_{lang}', '') or self.name

    def get_description(self, lang='uz'):
        """So'ralgan tildagi tavsifni qaytaradi"""
        return getattr(self, f'description_{lang}', '') or self.description_uz

    def get_address(self, lang='uz'):
        if lang == 'uz':
            return self.address
        return getattr(self, f'address_{lang}', '') or self.address

    @property
    def cover_image(self):
        img = self.images.filter(is_cover=True).first()
        if not img:
            img = self.images.first()
        return img


class HotelImage(models.Model):
    hotel    = models.ForeignKey(Hotel, related_name='images', on_delete=models.CASCADE,
                                 verbose_name="Mehmonxona")
    image    = models.ImageField(upload_to='hotels/', verbose_name="Rasm")
    is_cover = models.BooleanField(default=False, verbose_name="Asosiy rasm?")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        verbose_name        = "Rasm"
        verbose_name_plural = "Rasmlar"
        ordering            = ['order']
        indexes = [
            models.Index(fields=['hotel', 'order'], name='hotel_image_order_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['hotel'],
                condition=models.Q(is_cover=True),
                name='one_cover_image_per_hotel',
            ),
        ]

    def __str__(self):
        label = "Asosiy" if self.is_cover else "Qoshimcha"
        return f"{self.hotel.name} — {label}"


class ContactMessage(models.Model):
    name       = models.CharField(max_length=100, verbose_name="Ism")
    email      = models.EmailField(verbose_name="Email")
    message    = models.TextField(verbose_name="Xabar")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False, verbose_name="O'qildi?")

    class Meta:
        verbose_name        = "Xabar"
        verbose_name_plural = "Xabarlar"
        ordering            = ['-created_at']
        indexes = [
            models.Index(fields=['is_read', '-created_at'], name='contact_read_created_idx'),
        ]

    def __str__(self):
        return f"{self.name} — {self.created_at.strftime('%d.%m.%Y %H:%M')}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlangan'),
        ('cancelled', 'Bekor qilingan'),
        ('completed', 'Yakunlangan'),
    ]

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='bookings',
        verbose_name="Foydalanuvchi",
    )
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name='bookings',
        verbose_name="Mehmonxona",
    )
    check_in = models.DateField(verbose_name="Kirish sanasi")
    check_out = models.DateField(verbose_name="Chiqish sanasi")
    guests = models.PositiveSmallIntegerField(default=1, verbose_name="Mehmonlar soni")
    total_price = models.PositiveIntegerField(verbose_name="Umumiy narx (UZS)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    guest_name = models.CharField(max_length=200, verbose_name="Mehmon ismi")
    guest_phone = models.CharField(max_length=20, verbose_name="Telefon")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bron"
        verbose_name_plural = "Bronlar"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at'], name='booking_user_created_idx'),
            models.Index(fields=['hotel', 'check_in'], name='booking_hotel_checkin_idx'),
            models.Index(fields=['status'], name='booking_status_idx'),
        ]

    def __str__(self):
        return f"{self.guest_name} → {self.hotel.name} ({self.check_in}–{self.check_out})"

    @property
    def nights(self):
        return (self.check_out - self.check_in).days
