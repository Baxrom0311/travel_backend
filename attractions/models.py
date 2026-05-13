from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Attraction(models.Model):
    name_uz = models.CharField(max_length=200, verbose_name="Nomi (UZ)")
    name_en = models.CharField(max_length=200, verbose_name="Nomi (EN)", blank=True)
    name_ru = models.CharField(max_length=200, verbose_name="Nomi (RU)", blank=True)
    icon = models.CharField(max_length=10, default='🏛️')
    
    description_uz = models.TextField(verbose_name="Tavsif (UZ)")
    description_en = models.TextField(verbose_name="Tavsif (EN)", blank=True)
    description_ru = models.TextField(verbose_name="Tavsif (RU)", blank=True)
    
    # Qo'shimcha ma'lumotlar
    history_uz = models.TextField(verbose_name="Tarix (UZ)", blank=True)
    history_en = models.TextField(verbose_name="Tarix (EN)", blank=True)
    history_ru = models.TextField(verbose_name="Tarix (RU)", blank=True)
    
    # Video
    video_url = models.URLField(verbose_name="Video URL (YouTube)", blank=True)
    
    # Joylashuv
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        verbose_name="Kenglik (lat)",
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        verbose_name="Uzunlik (lng)",
    )
    
    # Ish vaqti va narx
    working_hours = models.CharField(max_length=100, blank=True, verbose_name="Ish vaqti")
    entrance_fee = models.PositiveIntegerField(default=0, verbose_name="Kirish narxi (UZS)")
    
    is_featured = models.BooleanField(default=False, verbose_name="Asosiy joylarda chiqsin?")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Diqqatga sazovor joy"
        verbose_name_plural = "Diqqatga sazovor joylar"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.icon} {self.name_uz}"
    
    @property
    def cover_image(self):
        """Asosiy rasmni qaytaradi"""
        cover = self.images.filter(is_cover=True).first()
        if cover:
            return cover
        return self.images.first()


class AttractionImage(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='attractions/', verbose_name="Rasm")
    caption_uz = models.CharField(max_length=200, blank=True, verbose_name="Izoh (UZ)")
    caption_en = models.CharField(max_length=200, blank=True, verbose_name="Izoh (EN)")
    caption_ru = models.CharField(max_length=200, blank=True, verbose_name="Izoh (RU)")
    is_cover = models.BooleanField(default=False, verbose_name="Asosiy rasm")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Rasm"
        verbose_name_plural = "Rasmlar"
        ordering = ['-is_cover', 'order']

    def save(self, *args, **kwargs):
        # Faqat bitta cover bo'lishi mumkin
        if self.is_cover:
            AttractionImage.objects.filter(attraction=self.attraction, is_cover=True).update(is_cover=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attraction.name_uz} - Rasm {self.order}"
