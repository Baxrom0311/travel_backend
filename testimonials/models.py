from django.db import models


class Testimonial(models.Model):
    """Foydalanuvchi sharhlari (home page'da ko'rsatish uchun)."""
    
    name = models.CharField(max_length=100, verbose_name="Ism")
    country = models.CharField(max_length=100, verbose_name="Davlat")
    role = models.CharField(max_length=100, blank=True, verbose_name="Kasb/lavozim")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Reyting (1-5)")
    
    text_uz = models.TextField(verbose_name="Matn (UZ)")
    text_en = models.TextField(blank=True, verbose_name="Matn (EN)")
    text_ru = models.TextField(blank=True, verbose_name="Matn (RU)")
    
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name="Avatar")
    
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    is_featured = models.BooleanField(default=False, verbose_name="Asosiy ro'yxatda")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Mijoz sharhi"
        verbose_name_plural = "Mijoz sharhlari"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.country})"
