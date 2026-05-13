from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class TransportRoute(models.Model):
    TYPE_CHOICES = [
        ('taxi',  'Taksi'),
        ('bus',   'Avtobus / Marshrutka'),
        ('train', 'Poyezd'),
    ]
    BADGE_STYLE_CHOICES = [
        ('recommended', 'Recommended'),
        ('budget', 'Budget'),
        ('comfort', 'Comfort'),
    ]

    transport_type   = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Transport turi")
    icon             = models.CharField(max_length=10, default='🚕')
    from_location_uz = models.CharField(max_length=200, verbose_name="Qaerdan (UZ)")
    from_location_en = models.CharField(max_length=200, verbose_name="Qaerdan (EN)", blank=True)
    from_location_ru = models.CharField(max_length=200, verbose_name="Qaerdan (RU)", blank=True)
    to_location_uz   = models.CharField(max_length=200, verbose_name="Qayerga (UZ)")
    to_location_en   = models.CharField(max_length=200, verbose_name="Qayerga (EN)", blank=True)
    to_location_ru   = models.CharField(max_length=200, verbose_name="Qayerga (RU)", blank=True)
    duration_min     = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Min vaqt (daqiqa)")
    duration_max     = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Max vaqt (daqiqa)")
    price_min        = models.PositiveIntegerField(verbose_name="Min narx (UZS)")
    price_max        = models.PositiveIntegerField(verbose_name="Max narx (UZS)")
    badge_uz         = models.CharField(max_length=50, default='', blank=True)
    badge_en         = models.CharField(max_length=50, default='', blank=True)
    badge_ru         = models.CharField(max_length=50, default='', blank=True)
    badge_style      = models.CharField(max_length=20, choices=BADGE_STYLE_CHOICES, default='recommended')
    description_uz   = models.TextField(verbose_name="Tavsif (UZ)")
    description_en   = models.TextField(verbose_name="Tavsif (EN)", blank=True)
    description_ru   = models.TextField(verbose_name="Tavsif (RU)", blank=True)
    order            = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name        = "Transport yo'nalishi"
        verbose_name_plural = "Transport yo'nalishlari"
        ordering            = ['order']
        indexes = [
            models.Index(fields=['transport_type', 'order'], name='transport_type_order_idx'),
        ]

    def __str__(self):
        return f"{self.icon} {self.get_transport_type_display()} | {self.price_min:,}–{self.price_max:,} UZS"

    def clean(self):
        errors = {}
        if self.duration_min and self.duration_max and self.duration_min > self.duration_max:
            errors['duration_min'] = "Min vaqt max vaqtdan katta bo'lmasligi kerak."
        if self.price_min is not None and self.price_max is not None and self.price_min > self.price_max:
            errors['price_min'] = "Min narx max narxdan katta bo'lmasligi kerak."
        if errors:
            raise ValidationError(errors)
