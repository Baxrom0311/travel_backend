from django.db import models
from django.core.validators import MinValueValidator


class Tour(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Oson'),
        ('medium', "O'rtacha"),
        ('hard', 'Qiyin'),
    ]
    DURATION_TYPE = [
        ('hours', 'Soat'),
        ('days', 'Kun'),
    ]

    title_uz = models.CharField(max_length=200, verbose_name="Sarlavha (UZ)")
    title_en = models.CharField(max_length=200, blank=True)
    title_ru = models.CharField(max_length=200, blank=True)

    slug = models.SlugField(unique=True)

    short_description_uz = models.TextField(max_length=300, verbose_name="Qisqa tavsif (UZ)")
    short_description_en = models.TextField(max_length=300, blank=True)
    short_description_ru = models.TextField(max_length=300, blank=True)

    description_uz = models.TextField(verbose_name="To'liq tavsif (UZ)")
    description_en = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)

    # Itinerary (kun-bakun)
    itinerary_uz = models.TextField(verbose_name="Kun-bakun rejasi (UZ)", blank=True)
    itinerary_en = models.TextField(blank=True)
    itinerary_ru = models.TextField(blank=True)

    cover_image = models.ImageField(upload_to='tours/', verbose_name="Asosiy rasm")

    # Narx va vaqt
    price = models.PositiveIntegerField(verbose_name="Narx (UZS)")
    duration = models.PositiveIntegerField(verbose_name="Davomiyligi")
    duration_type = models.CharField(max_length=10, choices=DURATION_TYPE, default='hours')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    
    max_people = models.PositiveIntegerField(default=20, verbose_name="Maks. kishi")
    min_people = models.PositiveIntegerField(default=1, verbose_name="Min. kishi")

    # Tarkib
    includes_uz = models.TextField(verbose_name="Narxga kiradi (UZ)", blank=True)
    includes_en = models.TextField(blank=True)
    includes_ru = models.TextField(blank=True)

    excludes_uz = models.TextField(verbose_name="Narxga kirmaydi (UZ)", blank=True)
    excludes_en = models.TextField(blank=True)
    excludes_ru = models.TextField(blank=True)

    meeting_point_uz = models.CharField(max_length=200, blank=True)
    meeting_point_en = models.CharField(max_length=200, blank=True)
    meeting_point_ru = models.CharField(max_length=200, blank=True)

    guide_languages = models.CharField(max_length=100, default='Uzbek, English', verbose_name="Gid tillari")

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0)])
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tur"
        verbose_name_plural = "Turlar"
        ordering = ['-is_featured', 'order']

    def __str__(self):
        return self.title_uz


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tours/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
