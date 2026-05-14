from django.db import models
from django.core.cache import cache


MAP_PROVIDERS = [
    ('carto_voyager', "CartoDB Voyager (default, chiroyli)"),
    ('carto_positron', "CartoDB Positron (light, minimal)"),
    ('carto_dark', "CartoDB Dark Matter (dark theme)"),
    ('stadia_alidade', "Stadia Alidade Smooth (premium look)"),
    ('stadia_outdoors', "Stadia Outdoors (terrain)"),
    ('stamen_toner', "Stamen Toner (black/white)"),
    ('stamen_terrain', "Stamen Terrain (relief)"),
    ('esri_satellite', "Esri World Imagery (sun'iy yo'ldosh)"),
    ('esri_streets', "Esri World Street Map"),
]


class SiteSettings(models.Model):
    """Singleton model - faqat 1 ta instance bo'lishi mumkin."""
    
    # Map settings
    map_provider = models.CharField(
        max_length=30,
        choices=MAP_PROVIDERS,
        default='carto_voyager',
        verbose_name="Xarita provayderi",
        help_text="Saytdagi barcha xaritalar uchun ishlatiladigan provayder",
    )
    map_dark_provider = models.CharField(
        max_length=30,
        choices=MAP_PROVIDERS,
        default='carto_dark',
        verbose_name="Dark mode xarita provayderi",
        help_text="Foydalanuvchi dark mode'da bo'lsa ishlatiladigan provayder",
    )
    map_default_zoom = models.PositiveIntegerField(
        default=13,
        verbose_name="Default zoom",
        help_text="Xarita boshlang'ich zoom darajasi (1-18)",
    )
    
    # Site info
    site_name = models.CharField(max_length=100, default='Visit Khorezm')
    site_tagline = models.CharField(max_length=200, blank=True, default='Travel & Tourism')
    site_description = models.TextField(blank=True, default='Xorazm viloyati turizm portali')
    
    # Contact
    contact_email = models.EmailField(default='info@visitkhorezm.uz')
    contact_phone = models.CharField(max_length=30, default='+998 61 226 56 56')
    contact_address = models.CharField(max_length=200, default='Xiva, Xorazm viloyati')
    
    # Social
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)
    
    # Meta
    maintenance_mode = models.BooleanField(
        default=False,
        help_text="Sayt nazorat rejimida bo'lsa, foydalanuvchilarga xabar ko'rsatiladi",
    )
    maintenance_message = models.TextField(
        blank=True,
        default="Sayt vaqtinchalik ishga yaroqsiz. Iltimos keyinroq qaytib keling.",
    )
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure singleton - only one instance
        if SiteSettings.objects.exists() and not self.pk:
            raise ValueError("SiteSettings singleton - faqat 1 ta instance bo'ladi")
        super().save(*args, **kwargs)
        cache.delete('site_settings')

    def delete(self, *args, **kwargs):
        # Prevent deletion
        pass

    @classmethod
    def get(cls) -> 'SiteSettings':
        """Get or create singleton instance with caching."""
        cached = cache.get('site_settings')
        if cached:
            return cached
        obj, _ = cls.objects.get_or_create(pk=1)
        cache.set('site_settings', obj, 30)  # 30 seconds
        return obj
